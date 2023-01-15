from bing_image_downloader import downloader
def DownloadImage(query, directory, amount):
  for i in range(amount):
    print(f"Download image {i} of {amount} for query {query}")
    downloader.download(query, limit=amount,
                        adult_filter_off=True,
                        output_dir=directory)