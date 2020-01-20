import logging
from urllib import request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
import re
import os
from scraper import models


class ScraperBaseError(Exception):
    pass


class ScraperFileSaveError(ScraperBaseError):
    pass


class ScraperRequestError(ScraperBaseError):
    pass


class ScraperFactoryError(ScraperBaseError):
    pass


class Scraper(object):
    _headers = {
        'user-agent':
            'Mozilla/5.0 (Macintosh;'
            ' Intel Mac OS X 10_11_6)'
            ' AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/53.0.2785.143 Safari/537.36'
    }
    scraper_type = None
    base_dir = "data"

    def __init__(self):
        self.beautiful_soup = None
        self.url = None
        self.site_name = None

    def set_url_and_site_name(self, url):
        self.url = url
        self.site_name = urlparse(self.url).netloc

    @property
    def resource_dir_path(self):
        return "{}/{}/{}".format(self.base_dir, self.site_name, self.scraper_type)

    def create_dirs(self):
        if not os.path.exists(self.resource_dir_path):
            os.makedirs(self.resource_dir_path)

    def _make_urlopen_request(self, url):
        """
        Download html from url.
        """
        try:
            requests = Request(url, headers=self._headers)
            html = urlopen(requests)
            html = html.read()
        except Exception as error:
            raise ScraperRequestError(error)
        return html

    def _set_beautiful_soup_content(self, html):
        """
        Create beautiful soup content.
        """
        try:
            self.beautiful_soup = BeautifulSoup(html, 'html.parser')
        except Exception as error:
            raise ScraperRequestError(error)

    def download_content(self, url):
        """
        Download content from url.
        """
        self.set_url_and_site_name(url)

        html = self._make_urlopen_request(url)
        self._set_beautiful_soup_content(html)

        self.create_dirs()

    def retrieve_resources(self, task):
        raise NotImplementedError

    def file_name(self, url_path, data_format):
        raise NotImplementedError


class TextScraper(Scraper):
    scraper_type = 'text'
    html_elements = ['style', 'script', 'meta', '[document]']
    file_format = '.txt'

    def tag_visible(self, element):
        if element.parent.name in self.html_elements:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_beautiful_soup(self):
        """
        Fetch text from beautiful soup content.
        """
        texts = self.beautiful_soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def file_name(self, url_path, data_format):
        """
        Convert and validate file name when is necesary
        """
        file_name = os.path.basename(url_path)

        if file_name == '':
            file_name = self.site_name

        file_name = file_name.replace("/", "_")

        if not file_name.endswith(data_format):
            file_name = file_name + data_format
        return file_name

    @staticmethod
    def write_to_file(dir_path, file_name, text):
        file = open("{}/{}".format(dir_path, file_name), "w+")
        file.write(text)
        file.close()

    def retrieve_resources(self, task):
        """
        Find all text fields and save to the file
        """
        file_name = self.file_name(self.url, self.file_format)

        path = "{}/{}".format(self.resource_dir_path, file_name)

        resource = models.Resource(
            site_name=self.site_name, path=path, type=self.scraper_type, task=task, file_name=file_name
        )
        try:
            #import pdb; pdb.set_trace()
            text = self.text_from_beautiful_soup()
            self.write_to_file(self.resource_dir_path, file_name, text)
            resource.set_status("Downloaded")
        except Exception as error:
            resource.set_status("Error: {}".format(error))
        resource.save()


class ImageScraper(Scraper):
    scraper_type = 'image'
    _availabe_image_formats = ['.jpg', '.png', '.bmp', '.svg']

    def file_name(self, url_path, data_format):
        """
        Reformat file name, when is necessary
        """
        file_name = os.path.basename(url_path).rstrip()
        if not file_name.endswith(data_format):
            file_name = file_name + data_format
        return file_name

    def _find_images_by_format(self, image_format):
        return self.beautiful_soup.find_all(
            'img', {'src': re.compile(image_format)}
        )

    @property
    def _find_all_types_images(self):
        """
        Return dictionary as {"format image": "array with images"}
        """
        images = {
            image_format: self._find_images_by_format(image_format)
            for image_format in self._availabe_image_formats
        }
        return images

    @staticmethod
    def _image_url(image, format_image, url, site_name):
        """
        Service few types common url patterns
        """
        url_path = image['src'] + '\n'
        logging.info("url_path:" + url_path)

        url_path = url_path.rstrip("\n")

        if url_path.startswith('/') and not url_path.startswith('//'):
            url_path = urlparse(url).scheme + "://" + site_name + url_path

        # url=//amazon.s3.test_url.with_some_file.jpg
        if url_path.startswith('//'):
            url_path = url_path.split('//')[1]
            url_path = urlparse(url).scheme + "://" + url_path

        if url_path.startswith(urlparse(url).scheme) and not url_path.endswith(format_image):
            url_path = url_path.split(format_image)[0] + format_image

        return url_path

    def try_retrieve_from_url(self, resource, url_path, file_name):
        """
        Try download image from url_path and save status in database
        """
        try:
            request.urlretrieve(url_path, "{}/{}".format(self.resource_dir_path, file_name))
            resource.set_status("Downloaded")
            resource.path = "{}/{}".format(self.resource_dir_path, file_name)
            logging.info("Downloaded {}".format(file_name))
        except Exception as error:
            resource.set_status("Error {}".format(error))
            resource.file_name = 'not_available'
            logging.info("Cannot download image from {}".format(url_path))

    def retrieve_resources(self, task):
        """
        Find all images in fetch html and try save image in storage
        """
        for format_image, images in self._find_all_types_images.items():
            for image in images:
                url_path = self._image_url(image, format_image, self.url, self.site_name)
                file_name = self.file_name(url_path, format_image)
                resource = models.Resource(site_name=self.site_name, type=self.scraper_type, task=task,
                                           file_name=file_name)
                self.try_retrieve_from_url(resource, url_path, file_name)
                resource.save()


class ScraperFactory(object):
    """
    Return scraper depand of required type
    """

    @staticmethod
    def get_scraper(scraper_type):
        if scraper_type == 'image':
            return ImageScraper()
        elif scraper_type == 'text':
            return TextScraper()
        else:
            raise ScraperFactoryError("Invalid scraper type !!!")
