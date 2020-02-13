import aiohttp
import fire
import asyncio
from timeit import default_timer

from iiif_image_api import IIIFImageApi


class TileTester:
    def __init__(self, dry_run: bool, workers: int):
        self._dry_run = dry_run
        self._workers = workers

    async def process(self, image_api_url: str, scale_factor_index: int = -1):
        print(f"processing {image_api_url} with {self._workers} workers.")

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            image_api = await self._get_image_api(image_api_url, session)

            if scale_factor_index > -1:
                await self._process_scalefactor(scale_factor_index, image_api, session)
            else:
                for i in range(len(image_api.ScaleFactors)):
                    await self._process_scalefactor(i, image_api, session)

    async def _get_image_api(self, image_api_url: str, session: aiohttp.ClientSession) -> IIIFImageApi:
        async with session.get(image_api_url) as response:
            return IIIFImageApi(await response.json())

    async def _process_scalefactor(self, scale_factor_index: int, image_api: IIIFImageApi, session: aiohttp.ClientSession):
        urls = image_api.get_urls_for_scalefactor(scale_factor_index)

        tasks = []

        start = 0
        end = 0
        if not self._dry_run:
            sem = asyncio.Semaphore(self._workers)
            start = default_timer()
            for url in urls:
                task = asyncio.create_task(self._get_tile(sem, url, session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            end = default_timer()

        print('\n'.join(urls))
        print(f"{len(urls)} tiles. scalefactor {scale_factor_index}. {end - start}s")
        print('------------')

    async def _get_tile(self, sem, url, session: aiohttp.ClientSession):
        async with sem:
            async with session.get(url) as response:
                return url


def process_batch(image_url="https://view.nls.uk/iiif/7443/74438561.5/info.json", scale_factor_index=-1, dry_run=False, workers=10):
    tile_tester = TileTester(dry_run, workers)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tile_tester.process(image_url, scale_factor_index))


if __name__ == '__main__':
    fire.Fire(process_batch)