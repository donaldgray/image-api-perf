import math


class IIIFImageApi:
    def __init__(self, json: dict):
        if not dict:
            return

        self.Width = int(json.get("width"))
        self.Height = int(json.get("height"))
        self.Id = json.get("@id")

        tiles = json.get("tiles", {})[0]
        self.ScaleFactors = tiles.get("scaleFactors")
        self.TileWidth = int(tiles.get("width"))
        self.TileHeight = int(tiles.get("height"))

    def get_urls_for_scalefactor(self, scale_factor_index: int = 0):
        scale_factor = self.ScaleFactors[scale_factor_index]

        urls = []

        full_width = math.ceil(self.Width / scale_factor)
        full_height = math.ceil(self.Height / scale_factor)

        tiles_x = math.ceil(full_width / self.TileWidth)
        tiles_y = math.ceil(full_height / self.TileHeight)

        for tx in range(tiles_x):
            for ty in range(tiles_y):
                x = tx * self.TileWidth
                y = ty * self.TileHeight
                w = self.TileWidth if x + self.TileWidth < full_width else full_width - x
                h = self.TileHeight if y + self.TileHeight < full_height else full_height - y

                urls.append(self._get_url(x, y, w, h, scale_factor))

        return urls

    def _get_url(self, x, y, tile_width, tile_height, scale_factor):
        return f"{self.Id}/{x * scale_factor},{y * scale_factor},{tile_width * scale_factor},{tile_height * scale_factor}/{self.TileHeight},/0/default.jpg"