odoo.define('imei_number_trackers.SaleImeiScreen', function (require) {
"use strict";
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var Dialog = require('web.Dialog');

var _t = core._t;
var QWeb = core.qweb;
    const { qweb } = require('web.core');
    const mobile = require('web_mobile.core');


// load widget with main barcode scanning View
var SaleImeiScreen = AbstractAction.extend({
    contentTemplate: 'SaleImeiScreen',
     events: {
        'click .imei_back_to_return': '_onClickReturnIMEI',
        'click .imei_sale_next_to_return' : '_onClickReturnIMEINext',
        'click .imei_sale_previous_to_return' : '_onClickReturnIMEIPrevious',
        'click  .button_is_typing_activated' : '_onClickVisibleTyping',
        'click  .add_screen_imei_sale_order' : '_onClickAddIntoList',
        'click  .imei_sale_delete' : '_onClickDeleteIMEI',
        'click .return_imei_mobile_scanner': '_onClickMobileCamera'


    },

    /**
     * @override
     */
 filter_IMEI_numbers : function(imei_return_list,product_id)
 {


 return imei_return_list.filter((imei) => imei.product_id[0] == product_id)





 },

 merge_same_order_line : function(order_list)
 {

var product_list = {}
for(let rec in order_list){
product_list[order_list[rec].product_id]  = 0

}


for(let rec in order_list){
product_list[order_list[rec].product_id] = product_list[order_list[rec].product_id] +order_list[rec].product_uom_qty



}

var ids = []
var order_list_new =[]
for (let rec  in order_list){

console.log('ids.includes(order_list[rec].product_id)' ,ids.includes(order_list[rec].product_id[0]))
console.log('ids',ids)



if (ids.includes(order_list[rec].product_id[0])){


}else{

ids.push(order_list[rec].product_id[0])
order_list[rec].product_uom_qty = product_list[order_list[rec].product_id]
order_list_new.push(order_list[rec] )

}


}




console.log('order_list_new',order_list_new)
return order_list_new
 },



    init: function(parent, action) {
        this._super.apply(this, arguments);

        this.id = action.context.active_id




    },



willStart: function() {
        var self = this;
        return this._super().then(async function() {

                    await self._rpc({
                    model: 'imei.number',
                    method: 'search_read',
                    domain: [['sale_order','=',self.id]],
                }).then(function (imei) {


                    self.imei_return_list = imei


                    });

               await self._rpc({
                    model: 'sale.order.line',
                    method: 'search_read',
                    domain: [['order_id','=',self.id],['product_id.is_imei_required','=',true]],
                }).then(function (Product) {


                                        self.products = self.merge_same_order_line(Product)





                    });

                self.current_products = self.products[0]
                console.log( self.current_products)

                self.current_position = 0
                self.page_number  = 1
                self.current_view_imei =self.filter_IMEI_numbers(self.imei_return_list,self.current_products.product_id[0])
                self.is_typing = false





            });



//        });

    },



      _onClickReturnIMEI: function(ev) {
        ev.preventDefault();
        if (this.isMultiSale_id) {
            // define action from scratch instead of using existing 'action_event_view' to avoid
            // messing with menu bar
            this.do_action({
                type: 'ir.actions.act_window',
                name: _t('Transfer Order'),
                res_model: 'sale.order',
                views: [
                    [false, 'kanban'],
                    [false, 'calendar'],
                    [false, 'list'],
                    [false, 'gantt'],
                    [false, 'form'],
                    [false, 'pivot'],
                    [false, 'graph'],
                    [false, 'map'],
                ],
                target:'main'
            });
        } else {
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'sale.order',
                res_id: this.id,
                views: [[false, 'form']],
                target:'main'
            });
        }
    },

    _onClickReturnIMEINext : function(ev){

if(this.products[this.current_position+1]){
//
this.current_position = this.current_position+1
this.current_products =this.products[this.current_position]
this.page_number = this.page_number + 1
this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])

//
//
}
        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));



},

_onClickReturnIMEIPrevious : function(ev){

if(this.products[this.current_position-1]){
//
this.current_position = this.current_position-1
this.current_products =this.products[this.current_position]
this.page_number = this.page_number - 1
this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])


//
//
}
        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));



},

remove_from_list:  function(imei_lists,imei_id){

   return imei_lists.filter((imei)=>imei.id != imei_id )
     },


_onClickDeleteIMEI : function(ev) {
var id =ev.currentTarget.getAttribute('id')


this._rpc({
                model: 'imei.number',
                method: 'imei_remove_imei',
                args: [[],id]
            })
            this.imei_return_list=this.remove_from_list(this.imei_return_list,ev.currentTarget.getAttribute('id'))
            this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])

        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));





            },









CheckBoundaryOfEntry : function(ev){


this.is_not_limit_crossed = !(this.current_products.product_uom_qty == this.current_view_imei.length)


},






_onClickAddIntoList : async function(ev){

this.CheckBoundaryOfEntry()

if (this.is_not_limit_crossed)
{
 var data = this.$('.imei_sale_input_texts').val()
console.log("data",data)
var self = this

var current_products=this.products[this.current_position].product_id[0]
console.log(current_products)
var current_picking_id =this.id
 await this._rpc({
                model: 'imei.number' ,
                               method: 'create_record',
                args: [[],data, current_picking_id, current_products]
            }).then(function (numbers) {

            self.imei_return_list.push(numbers)
                    });


this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])




}

        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));



},












async _onClickMobileCamera(event) {





this.CheckBoundaryOfEntry()

            var get_response = await mobile.methods.scanBarcode();
            var data = get_response.data
if (this.is_not_limit_crossed)
{

var self = this
var current_products=this.products[this.current_position].product_id[0]
var current_picking_id =this.id
 await this._rpc({
                model: 'imei.number',
                method: 'create_record',
                args: [[],data, current_picking_id, current_products]
            }).then(function (numbers) {

            self.imei_return_list.push(numbers)
                    });


this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])




}

        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));






},





_onClickVisibleTyping : function(ev){
this.is_typing = this.is_typing? false : true
        this.$el.html(QWeb.render("ImeiReturnScreen", {widget: this}))

},



    start: function() {
        core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
    },

    /**
     * @override
     */
    destroy: function () {
        core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
        this._super();
    },
  _onBarcodeScanned: async function(barcode) {


this.CheckBoundaryOfEntry()
//alert(barcode)
            var data = barcode
if (this.is_not_limit_crossed)
{

var self = this
var current_products=this.products[this.current_position].product_id[0]
var current_picking_id =this.id
 await this._rpc({
                model: 'imei.number',
                method: 'create_record',
                args: [[],barcode, current_picking_id, current_products]
            }).then(function (numbers) {

            self.imei_return_list.push(numbers)
                    });



this.current_view_imei =this.filter_IMEI_numbers(this.imei_return_list,this.current_products.product_id[0])




}

        this.$el.html(QWeb.render("SaleImeiScreen", {widget: this}));






}








});

core.action_registry.add('imei_number_trackers.SaleImeiScreen', SaleImeiScreen);

return SaleImeiScreen;

});