# Hoover
Python based scraper created using Scrapy and Splash.
### Requried Libraries and packages
  - Python 2.7+
  - Docker
### Installation and Usage on Ubuntu/OS X
1) Clone the hoover repository.
    ```sh
    $ git clone https://github.com/visimagic/hoover.git
    ```
2) Navigate to "tools" directory and execute `js.sh` and `scrape.sh`
    ```sh
    $ sudo ./scrape.sh
    $ sudo ./js.sh
    ```
3) After both scripts have completed downloading and installing the required packages, continue to [Docker](https://store.docker.com/search?type=edition&offering=community)  and download and install the respective edition of Docker.
4) After docker has completed downloading continue to install the Splash Image requried by following the offical Documentation for [Splash]( http://splash.readthedocs.io/en/latest/install.html).

5) Confirm Splash is up and running by issuing this commands via the Terminal.
    ```sh
    $ docker run -it -p 8050:8050 scrapinghub/splash --disable-private-mode
    ```
    Navigate to `http://localhost:8050` via the browser to ensure Splash is up and running.
6) Once the `Splash` server is running, we can begin using our Crawler. Navigate to the `hoover\woolworths` via the Terminal. Before running the Crawler, make sure all the below options are set accordingly:
    - In `settings.py` change `IMAGES_STORE` to a new path.
    - In `proxy.py` change the proxy list IP's. Currently `proxies.py` is not         being used but can be implemented by updating the `proxy_list` and including     it within the `DOWNLOADER_MIDDLEWARES =             {'woolies.proxy.RandomProxyMiddleware':100}`.

7) We can now start scraping by issuing the following commands (dependant on scenario) Navigate once again to the home directory of `hoover\woolworths` and issue the following command.
    ```sh
    $ scrapy crawl woolworths
    ``` 
    The above command is always issued first. It begins `Spider 1`, which is responsible for downloading the individual prodcut pages. The output of this scraper can be found within `hoover\woolworths\woolworths_products_url_crawl.txt` and will look something like this.
    ```sh
    https://www.woolworths.com.au/shop/productdetails/120384/watermelon-red-seedless
    https://www.woolworths.com.au/shop/productdetails/149820/strawberry-fruit-pot-organic
    https://www.woolworths.com.au/shop/productdetails/169792/blueberry-fresh
    https://www.woolworths.com.au/shop/productdetails/259421/mandarin-clementine
    ``` 
    Next we can run our second Spider `Spdier 2`, which will download and save the image, name and a brief description of the product. 
    To start `Spider 2` we issue the following command AFTER the `Spdier 1` has completed its job.
    ```sh
    $ scrapy crawl prod_wool -o output.csv
    ```
    
    `output.csv` has 6 columns out of which 3 are of interest, `name`, `desc` and `image_path`. All of these are self-explanatory, `output.csv` also contains, `images_url` which can be used to download images at a later time or used for cross-referencing purposes.

8) Further work can be done to make the process more streamlined but in its current state it achieves its purpose.




