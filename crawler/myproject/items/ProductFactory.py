from myproject.items.MagentoProductItem import MagentoSimpleProductItem, MagentoConfigurableProductItem, MagentoBaseProductItem
import time

class ProductFactory():

    def CreateMangentoProduct(self):
        current_timestamp = time.strftime("%Y-%m-%d")
        item = MagentoBaseProductItem()
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