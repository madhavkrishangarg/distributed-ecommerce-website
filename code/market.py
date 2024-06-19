import uuid

from concurrent import futures
import logging

import grpc
import market_pb2
import market_pb2_grpc

MAXSERVERS = 10
CONNECTIONS={}

class Market(market_pb2_grpc.MarketplaceServicer):
    seller_list = []
    items_list = []
    buyer_wishlist = []
    item_id_counter=0
    item_rating = {}
    
    def verify_seller(self, seller_address, seller_uuid, item_id):
        for item in self.items_list:
            if item["seller_address"] == seller_address and item["seller_uuid"] == seller_uuid and item["item_id"] == item_id:
                return True
        return False
    
    def registerSeller(self, request, context):
        seller_uuid = request.uuid
        seller_address = request.address
        try:
            if len(self.seller_list) < MAXSERVERS and ({seller_uuid: seller_address} not in self.seller_list):
                self.seller_list.append({seller_uuid: seller_address})
                print(f"Seller join request from {seller_address}, uuid={seller_uuid}")
                print(self.seller_list)
                return market_pb2.registerSellerResponse(success=True)
            else:
                return market_pb2.registerSellerResponse(success=False)
        except Exception as e:
            print(e)
            return market_pb2.registerSellerResponse(success=False)
        
    def notifyClient(ip_address, port, message):
        channel = grpc.insecure_channel(ip_address+":"+port)
        stub = market_pb2_grpc.MarketplaceStub(channel)
        response = stub.notifyClient(market_pb2.notifyClientRequest(message=message))
        print("Send to client: " + response.message)
        
    def sellItem(self, request, context):
        if({request.seller_uuid: request.seller_address} not in self.seller_list):
            return market_pb2.sellItemResponse(success=False,item_id=None)
        print(request.__str__())
        
        item_name = request.name
        category= "electronics" if request.electronics else ("fashion" if request.fashion else "other")
        quantity = request.quantity
        description = request.description
        seller_address = request.seller_address
        price = request.price
        seller_uuid = request.seller_uuid
        self.item_id_counter += 1
        try:
            self.items_list.append({"item_id": self.item_id_counter,"name": item_name, "category": category, "quantity": quantity, "description": description, "seller_address": seller_address, "price": price, "seller_uuid": seller_uuid})
            print(f"Sell item request from {seller_address}, uuid={seller_uuid}")
            print(self.items_list)
            return market_pb2.sellItemResponse(success=True,item_id=self.item_id_counter)
        except Exception as e:
            print("error :", e)
            return market_pb2.sellItemResponse(success=False,item_id=None)
        
    def updateItem(self, request, context):
        item_id=request.item_id
        # if(request.price):
        price=request.price
        # if(request.quantity):
        quantity=request.quantity
        # if(request.description):
        description=request.description
        # print(price,quantity,description)
        print(f"Update item request from {request.seller_address}")
        try:
            if self.verify_seller(request.seller_address, request.seller_uuid, item_id):
                print(f"seller verified {request.seller_address}")
                for item in self.items_list:
                    if item["item_id"] == item_id:
                        if(price is not None and price>0):
                            item["price"]=price
                            # price=item["price"]
                        if(quantity is not None and quantity>0):
                            item["quantity"]=quantity
                            # quantity=item["quantity"]
                        if(description is not None and len(description)>0):
                            item["description"]=description
                            # description=item["description"]
                        print(f"Item with id={item_id} updated by {request.seller_address}")
                        price=item["price"]
                        quantity=item["quantity"]
                        description=item["description"]
                        # print(price,quantity,description)
                        for wish in self.buyer_wishlist:
                            if wish["item_id"] == item_id:
                                message=f"Item with id={item_id} updated by {request.seller_address}, new price={price}, new quantity={quantity}, new description={description}"
                                try:
                                    self.notifyBuyer(message, wish["buyer_address"])
                                except Exception as e:
                                    print("error :", e, "unable to notify buyer")
                                
                        return market_pb2.updateItemResponse(success=True)
            else:
                return market_pb2.updateItemResponse(success=False)
        except Exception as e:
            print("error: ", e)
            return market_pb2.updateItemResponse(success=False)


    def deleteItem(self, request, context):
        item_id=request.item_id
        if(self.verify_seller(request.seller_address,request.seller_uuid,item_id)):
            for item in self.items_list:
                if item["item_id"] == item_id:
                    self.items_list.remove(item)
                    return market_pb2.deleteItemResponse(success=True)
        else:
            return market_pb2.deleteItemResponse(success=False)
            
    def displaySellerItems(self, request, context):
        seller_uuid=request.seller_uuid
        seller_address=request.seller_address
        print(f"Display seller items request from {seller_address}, uuid={seller_uuid}")
        try:
            
            for item in self.items_list:
                if item["seller_address"] == seller_address and item["seller_uuid"] == seller_uuid:
                    # product=market_pb2.Item(name=item["name"], electronics=item["category"]=="electronics", fashion=item["category"]=="fashion", other=item["category"]=="other", quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=calculateRating(item["item_id"]))
                    print(item["item_id"])
                    # print(self.calculateRating(item["item_id"]))
                    if(item["category"]=="electronics"):
                        product=market_pb2.Item(name=item["name"], electronics=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    elif(item["category"]=="fashion"):
                        product=market_pb2.Item(name=item["name"], fashion=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    else:
                        product=market_pb2.Item(name=item["name"], other=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    # print(product.__str__())
                    yield product

        except Exception as e:
            print("error: ", e)
            item = market_pb2.Item(item_id=None)
            yield item
        
        
    def searchItem(self, request, context):
        item_category = "electronics" if request.electronics else ("fashion" if request.fashion else ("other" if request.other else "any"))
        item_name = request.name
            
        try:
            for item in self.items_list:
                if (item["name"] == item_name or not item_name) and (item["category"] == item_category or item_category=="any"):
                    if(item["category"]=="electronics"):
                        product=market_pb2.Item(name=item["name"], electronics=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    elif(item["category"]=="fashion"):
                        product=market_pb2.Item(name=item["name"], fashion=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    else:
                        product=market_pb2.Item(name=item["name"], other=True, quantity=item["quantity"], description=item["description"], seller_address=item["seller_address"], seller_uuid=item["seller_uuid"], price=item["price"], item_id=item["item_id"], rating=self.calculateRating(item["item_id"]))
                    print(product.__str__())
                    yield product
                    
        except Exception as e:
            print("error: ", e)
            yield market_pb2.Item(item_id=None)
            
    def buyItem(self, request, context):
        item_id=request.item_id
        quantity=request.quantity
        buyer_addr=request.address
        
        try:
            for item in self.items_list:
                if item["item_id"] == item_id:
                    if item["quantity"] >= quantity:
                        item["quantity"] -= quantity
                        #remove from wishlist
                        for wish in self.buyer_wishlist:
                            if wish["item_id"] == item_id:
                                self.buyer_wishlist.remove(wish)

                        message=f"Item with id={item_id} bought by {buyer_addr}, quantity={quantity}"
                        try:
                            self.notifySeller(message, item["seller_address"])
                        except Exception as e:
                            print("error :", e, "unable to notify seller")
                        
                        print(self.items_list)
                        return market_pb2.buyItemResponse(success=True)
                    else:
                        return market_pb2.buyItemResponse(success=False)
        except Exception as e:
            print("error :", e)
            return market_pb2.buyItemResponse(success=False)
        
    def addToWishlist(self, request, context):
        item_id=request.item_id
        buyer_address=request.address
        try:
            for item in self.items_list:
                if item["item_id"] == item_id:
                    self.buyer_wishlist.append({"item_id": item_id, "buyer_address": buyer_address})
                    print(self.buyer_wishlist)
                    return market_pb2.addToWishlistResponse(success=True)
            else:
                return market_pb2.addToWishlistResponse(success=False)
        except Exception as e:
            print("error :", e)
            return market_pb2.addToWishlistResponse(success=False)
        
    def rateItem(self, request, context):
        item_id=request.item_id
        rating=request.rating
        address=request.address
        try:
            # print([item["item_id"] for item in self.items_list])
            if(item_id not in [item["item_id"] for item in self.items_list]):
                print("item not found")
                return market_pb2.rateItemResponse(success=False)
            
            if(not item_id in self.item_rating):
                self.item_rating[item_id]=[]

            for rate in self.item_rating[item_id]:
                if rate["address"]==address:
                    return market_pb2.rateItemResponse(success=False)
            
            self.item_rating[item_id].append({"address":address,"rating":rating})
            print(self.item_rating)
            return market_pb2.rateItemResponse(success=True)
        except Exception as e:
            print("error :", e)
            return market_pb2.rateItemResponse(success=False)

    def calculateRating(self, item_id):
        try:
            if(not item_id in self.item_rating):
                return 0
            else:
                total=0
                for rate in self.item_rating[item_id]:
                    total+=rate["rating"]
                return int(total/len(self.item_rating[item_id]))
        except Exception as e:
            print("error :", e)
            return 0

    def notifySeller(self, message, seller_address):
        channel = grpc.insecure_channel(seller_address)
        stub = market_pb2_grpc.MarketplaceStub(channel)
        response = stub.notifySeller(market_pb2.notifySellerRequest(msg=message))
        print("Send to seller: " + message)
        if response.success:
            print(f"Notification sent successfully")
        else:
            print(f"Failed to send notification")
        return
    
    def notifyBuyer(self, message, buyer_address):
        channel = grpc.insecure_channel(buyer_address)
        stub = market_pb2_grpc.MarketplaceStub(channel)
        response = stub.notifyBuyer(market_pb2.notifyBuyerRequest(msg=message))
        print("Send to buyer: " + message)
        if response.success:
            print(f"Notification sent successfully")
        else:
            print(f"Failed to send notification")
        return


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketplaceServicer_to_server(Market(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()