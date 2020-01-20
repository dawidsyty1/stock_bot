from django.test import TestCase
from scraper import scrapers, models
from unittest.mock import patch


class ScraperTests(TestCase):

    def setUp(self):
        self.scraper = scrapers.Scraper()

    def test_set_url_and_site_name(self):
        """
        Set url and site name in class member
        """
        url = "https://www.freeimages.com/photo/xmas-bunny-1313404"

        self.scraper.set_url_and_site_name(url)
        self.assertEqual(self.scraper.url, url)
        self.assertEqual(self.scraper.site_name, "www.freeimages.com")

    def test_download_content_corrupted_url(self):
        """
        Test corrupted url and exceptions
        """
        url = "https://www.freeimages.c"
        with self.assertRaises(scrapers.ScraperRequestError):
            self.scraper._make_urlopen_request(url)

    def test_set_fake_beautiful_soup_content(self):
        """
        Test beautiful soup exception.
        """
        with self.assertRaises(scrapers.ScraperRequestError):
            self.scraper._set_beautiful_soup_content(None)


class TextScraperTest(TestCase):
    fixtures = ["resourses.json", "tasks.json"]
    example_html = """
    <table>
        <thead>
            <tr class="myClass">
                <th>Test</th>
                <th>to</th>
                <th>find</th>
                <th>Text</th>
            </tr>
        </thead>
    </table>
    """

    basic_url = "https://www.freeimages.com/photo/xmas-bunny-1313404"

    def setUp(self):
        self.scraper = scrapers.TextScraper()

    def test_text_from_beautiful_soup(self):
        """
        Test text finder
        """
        self.scraper._set_beautiful_soup_content(self.example_html)
        text = self.scraper.text_from_beautiful_soup()
        self.assertEqual(text, "   Test  to  find  Text   ")

    def test_tag_visible(self):
        """
        Test tags visible.
        """
        self.scraper._set_beautiful_soup_content(self.example_html)
        texts = self.scraper.beautiful_soup.findAll(text=True)
        self.assertEqual(self.scraper.tag_visible(texts[0]), False)
        self.assertEqual(self.scraper.tag_visible(texts[4]), True)

    def test_file_name(self):
        """
        Test file name setter.
        """
        file_name = self.scraper.file_name(self.basic_url, ".txt")
        self.assertEqual(file_name, "xmas-bunny-1313404.txt")
        url = "https://www.freeimages.com"
        file_name = self.scraper.file_name(url, ".txt")
        self.assertEqual(file_name, "www.freeimages.com.txt")

    @patch("scraper.scrapers.TextScraper.text_from_beautiful_soup")
    def test_retrieve_resources_not_dir(self, text):
        """
        Test retrieve resource method, in case when directory not exist.
        """
        text.return_value = "Text do przetestowania"

        self.scraper.set_url_and_site_name(self.basic_url)
        task = models.Task()
        task.save()

        self.scraper.retrieve_resources(task)

        resources = models.Resource.objects.filter(task=task.pk).first()
        self.assertEqual(
            resources.status,
            'Error: [Errno 2] No such file or directory: \'data/www.freeimages.com/text/xmas-bunny-1313404.txt\''
        )

    @patch("scraper.scrapers.TextScraper.text_from_beautiful_soup")
    @patch("scraper.scrapers.TextScraper.write_to_file")
    def test_retrieve_resources_success(self, text, write_to_file):
        """
        Test retrieve resource method, in case when everythings is ok
        """
        text.return_value = "Text do przetestowania"
        write_to_file.return_value = True

        self.scraper.set_url_and_site_name(self.basic_url)

        task = models.Task()
        task.save()

        self.scraper.retrieve_resources(task)
        #import pdb; pdb.set_trace()
        resources = models.Resource.objects.filter(task=task.pk).first()
        self.assertEqual(resources.status, "Downloaded")


class ImageScraperTest(TestCase):
    example_html = """<html>
                        <body>
                        
                        <img src="smiley.jpg" alt="Smiley face" width="42" height="42">
                        <img src="smiley_test_image.png" alt="Smiley face" width="42" height="42">
                        <img src="smil123ey.jpg" alt="Smiley face" width="42" height="42">
                        <img src="smil123ey.fake" alt="Smiley face" width="42" height="42">
                        </body>
                        </html>
                    """
    basic_url = "https://www.freeimages.com/photo/xmas-bunny-1313404"

    def setUp(self):
        self.scraper = scrapers.ImageScraper()

    @patch("urllib.request.urlretrieve", return_value=True)
    def test_retrieve_resources_success(self, urlretrieve):
        """
        Test general mechanism for retrieve resources from html using beautiful soup.
        """
        self.scraper._set_beautiful_soup_content(self.example_html)
        task = models.Task()
        task.save()
        for format_image, images in self.scraper._find_all_types_images.items():
            for image in images:
                self.scraper.set_url_and_site_name(self.basic_url)
                url_path = self.scraper._image_url(image, format_image, self.scraper.url, self.scraper.site_name)
                file_name = self.scraper.file_name(url_path, format_image)
                resource = models.Resource(site_name=self.scraper.site_name, type=self.scraper.scraper_type, task=task,
                                           file_name=file_name)
                self.scraper.try_retrieve_from_url(resource, url_path, file_name)
                resource.save()

        resources = models.Resource.objects.all().count()
        self.assertEqual(resources, 3)

    def test_image_url(self):
        """
        Image_url should return full image path.
        """
        image = {'src': self.basic_url + "/image.jpg"}
        path = self.scraper._image_url(image, ".jpg", self.basic_url, "www.freeimages.com")
        self.assertEqual(path, self.basic_url + "/image.jpg")

    def test_image_url_without_format(self):
        """
        Image_url should add image format.
        """
        image = {'src': self.basic_url + "/image"}
        path = self.scraper._image_url(image, ".jpg", self.basic_url, "www.freeimages.com")
        self.assertEqual(path, self.basic_url + "/image.jpg")

    def test_find_all_types_images(self):
        """
        Fetch all images from beautiful soup content.
        """
        self.scraper._set_beautiful_soup_content(self.example_html)
        self.scraper.set_url_and_site_name(self.basic_url)
        images = self.scraper._find_all_types_images
        self.assertEqual(2, len(images['.jpg']))
        self.assertEqual(1, len(images['.png']))
