import time


# class PrintMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.method == "POST":

#             print(request.method)
#         response = self.get_response(request)
#         print("------- PrintMiddleware ---------")

#         return response
