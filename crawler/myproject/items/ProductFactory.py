from myproject.items.BaseProductItem import BaseProductItem
from myproject.items.SimpleProductItem import SimpleProductItem
from myproject.items.ConfigurableProductItem import ConfigurableProductItem
import time

class ProductFactory():

    def create_base_product_item(self):
        current_timestamp = time.strftime("%Y-%m-%d")
        item = BaseProductItem()
        item["store"] = "admin"
        item["websites"] = "base"
        item["has_options"] = 0
        item["page_layout"] = "No layout updates"
        item["options_container"] = "Product Info Column"
        item["msrp_enabled"] = "Use config"
        item["msrp_display_actual_price_type"] = "Use config"
        item["gift_message_available"] = "No"
        item["min_qty"] = 0
        item["use_config_min_qty"] = 1
        item["is_qty_decimal"] = 0
        item["backorders"] = 0
        item["use_config_backorders"] = 1
        item["min_sale_qty"] = 1
        item["use_config_min_sale_qty"] = 1
        item["max_sale_qty"] = 0
        item["use_config_max_sale_qty"] = 1
        item["use_config_notify_stock_qty"] = 1
        item["manage_stock"] = 0
        item["use_config_manage_stock"] = 1
        item["stock_status_changed_auto"] = 0
        item["use_config_qty_increments"] = 1
        item["qty_increments"] = 0
        item["use_config_enable_qty_inc"] = 1
        item["enable_qty_increments"] = 0
        item["is_decimal_divided"] = 0
        item["stock_status_changed_automatically"] = 0
        item["use_config_enable_qty_increments"] = 1
        item["weight"] = 1
        item["qty"] = 100
        item["is_in_stock"] = 1
        item["status"] = "Disabled"

        item["feed_updated_date"] = current_timestamp
        item["created_date"] = current_timestamp
        return item


    def CreateSimpleMagentoProduct(self):
        pass

    def CreateConfigurableMagentoProduct(self):
        pass

    def create_simple_product_item(self, BaseItem):
        simple_item = SimpleProductItem(BaseItem)
        simple_item["type"] = "simple"
        simple_item["attribute_set"] = "Default"
        simple_item["visibility"] = "Catalog, Search"
        return simple_item

    def get_configurable_product_item(self, BaseItem, attribute_set, configurable_attributes):
        configurable_item = ConfigurableProductItem(BaseItem)
        configurable_item["type"] = "configurable"
        configurable_item["configurable_attributes"] = configurable_attributes
        configurable_item["attribute_set"] = attribute_set
        configurable_item["visibility"] = "Catalog, Search"
        return configurable_item

    def get_simple_variant_product_item(self, BaseItem, variant):

        #create sub sku for variants
        if (variant.color is not None):
            variant.sku = variant.sku + "_" + variant.color
        if (variant.size is not None):
            variant.sku = variant.sku + "_" + variant.size

        simple_variant_product_item = SimpleProductItem(BaseItem)
        simple_variant_product_item["sku"] = variant.sku
        simple_variant_product_item["color"] = variant.color
        simple_variant_product_item["size"] = variant.size
        simple_variant_product_item["type"] = "simple"
        simple_variant_product_item["attribute_set"] = variant.attribute_set
        simple_variant_product_item["configurable_attributes"] = variant.configurable_attributes
        simple_variant_product_item["visibility"] = "Not Visible Individually"
        return simple_variant_product_item