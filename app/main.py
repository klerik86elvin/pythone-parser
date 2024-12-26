from parsers.tap_az_parser import TapAzParser
from parsers.yeniemlak_parser import YeniemlakParser
from managers.filter_manager import FilterManager
from adapters.tap_data_transformer import TapDataTransformer
from url_generators.yeniemlak_az_url_generator import YeniemlakAzURLGenerator
from url_generators.tap_az_url_generator import TapAzURLGenerator
from enums.real_estate_type import RealEstateType
from enums import RealEstateType, AdType
from helpers.parser_helper import save_html_to_file
import json
import os
os.chdir("/home/ubuntu/pythone-parser")


with open("output.html", "r") as file:
    html_doc = file.read()

with open("static_data/yeniemlak.az/real_estate_config.json", "r", encoding="utf-8") as file:
    yeniemla_config = json.load(file)

with open("static_data/tap.az/real_estate_config.json", "r", encoding="utf-8") as file:
    tap_config = json.load(file)
    
# yeniemlak_parser = YeniemlakParser(yeniemla_config)
tap_parser = TapAzParser(tap_config)


# filter_manager = FilterManager(tap_parser.get_site_specific_filters())
# # filter_manager.set_filter('building_type', RealEstateType.APARTMENT.value)
# filter_manager.set_filter('ad_type', AdType.SALE.value)
# yeniemlak_url_generator = YeniemlakAzURLGenerator(tap_parser.get_base_url(), filter_manager.format_selected_filters())
# tap_url_generator = TapAzURLGenerator(tap_parser.get_base_url() ,filter_manager.format_selected_filters())

# url = tap_url_generator.generate_url()
# html = tap_parser.fetch_html("https://tap.az/elanlar/dasinmaz-emlak/torpaq-sahesi/43414570")
# save_html_to_file(html)
# # url = "https://tap.az/elanlar/dasinmaz-emlak/menziller"

parse_data = tap_parser.parse_detail_page("https://tap.az/elanlar/dasinmaz-emlak/heyet-evleri/38241132")
adapter = TapDataTransformer(parse_data, tap_config)
adapter.adapt()