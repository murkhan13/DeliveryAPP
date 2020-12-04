from itertools import chain
import json

from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework import filters

from django.shortcuts import get_object_or_404
from django.utils import timezone as djangotime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Prefetch, Q, FilteredRelation

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter

from cronProjectAPI.settings import ALLOWED_HOSTS
from .serializers import *
from .models import *
from knox.auth import TokenAuthentication




class DishDetailView(RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishDetailSerializer
    permission_classes = (AllowAny,)


class CategoryItemsView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSerializer
    permission_classes = (AllowAny,)

    def get(self, request,*args, **kwargs):
        return self.list(request, *args, **kwargs)


class SearchInRestaurantView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSearchSerializer
    # filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ['dishes__title']

    def get(self, request, *args, **kwargs):
        if 'search' in self.request.GET:
            search_term = self.request.GET['search']
            if search_term != '':
                restaurant_title = self.request.GET['restaurant']

                category_names = []
                categorees = Category.objects.filter(dishes__title__icontains=search_term)
                for i in range(len(categorees)):
                    category_names.append(categorees[i])

                # filtering given categories query for particular dishes,
                # and exclude categories with other names
                restaurant_obj = Restaurant.objects.get(title=restaurant_title)

                categories = Category.objects.prefetch_related(
                    Prefetch('dishes', queryset=Dish.objects.filter(title__icontains=search_term), to_attr='filtered_dishes')
                ).filter(name__in=category_names).filter(restaurants__restaurant=restaurant_obj)

                serializer = CategoryItemsSearchSerializer(categories, many=True, context={'request': request})

                return Response(serializer.data)
            else:
                return Response({
                    'status': False,
                    "detail": "Поле поиска пустое, попробуйте ещё раз"
                })
        else:
            return Response({
                "status": False,
                "detail": "Ничего не найдено."
            })


class SearchingCategoriesView(APIView):
    """
    Class Based View that handles parsing a searching categories

    Args:
        APIView ([class]): [view class from rest framework]

    Returns:
        [json object]: [json object of searching categories]
    """

    def get(self, request, *args, **kwargs):
        searching_categories = SearchingCategory.objects.all()
        serializer = SearchingCategoriesSerializer(searching_categories, many=True, context={'request': request})
        return Response(serializer.data)

class GlobalSearchView(APIView):
    """
    Class Based View that handles a searching through all restaurants logic

    Args:
        APIView ([class]): [view class from rest framework]

    Returns:
        [json object]: [json object of searched queryset]
    """
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        if 'search' in self.request.GET:
            search_term = self.request.GET['search']
            page = self.request.GET['page'] #.getlist('page', 1)
            if search_term != '':
                # restaurant_title = self.request.GET['rest_title']
                print("search:", search_term)

                category_names = []
                categorees = Category.objects.filter(dishes__title__icontains=search_term)
                for i in range(len(categorees)):
                    category_names.append(categorees[i])

                # filtering given categories query for particular dishes,
                # and exclude categories with other names
                # restaurant_obj = Restaurant.objects.get(title=restaurant_title)
                '''
                queryset = RestaurantMenu.objects.prefetch_related(
                    Prefetch('categories', queryset=Category.objects.prefetch_related(
                        Prefetch('dishes', queryset=Dish.objects.filter(title__icontains=search_term), to_attr='filtered_dishes')
                    ).filter(name__in=category_names), to_attr='filtered_categories')
                ).filter(categories__name__in = category_names)

                serializer = GlobalSearchSerializer(queryset, many=True, context={'request': request})'''

                dishes = Dish.objects.filter(
                    Q(title__icontains=search_term) |
                    Q(category__name__icontains=search_term)
                )
                if len(dishes) == 0:
                    return Response({
                        'status': False,
                        'detail': "По данному запросу ничего не было найдено."
                    })
                else:
                    categories_qs = []
                    for category in Category.objects.all():
                        for dish in dishes:
                            if category in dish.category.all():
                                if category not in categories_qs:
                                    categories_qs.append(category)
                    final_list = []
                    restaurantmenu_qs = RestaurantMenu.objects.filter(categories__in=categories_qs).distinct()
                    restaurantmenu_qs = restaurantmenu_qs.filter(restaurant__worksFrom__lt=timezone.now().time()).filter(restaurant__worksTo__gt=timezone.now().time())
                    print('time:', timezone.now().time())
                    paginator = Paginator(restaurantmenu_qs, 10)
                    restaurantmenu_qs = paginator.page(page)
                    search_response_dict = {}
                    pagination_dict = {"param": "page", "count": paginator.num_pages, "current": int(page), "rows": 10}
                    for restaurantmenu in restaurantmenu_qs:
                        categorees = restaurantmenu.categories.all()
                        rest_dict = {}
                        restaurant_qs = Restaurant.objects.filter(title=restaurantmenu.restaurant.title)
                        restaurant_dishes = Dish.objects.filter(title__icontains=search_term, category__in=categorees)
                        rest_dict['restaurant'] = RestaurantDetailSerializer(restaurant_qs, many=True, context={'request':request}).data[0]
                        rest_dict['dishes'] = DishDetailSerializer(restaurant_dishes, many=True, context={'request':request}).data
                        final_list.append(rest_dict)
                    search_response_dict["search_response"] = final_list
                    if len(final_list) > 0 :
                        search_response_dict['pagination'] = pagination_dict
                    else:
                        return Response({
                            'status': False,
                            'detail': "По данному запросу ничего не было найдено."
                        })
                    return Response(search_response_dict)
            else:
                return Response({
                    'status': False,
                    'detail': 'Поле поиска пустое, попробуйте ещё раз'
                })
        else:
            return Response({
                "status": False,
                "detail": "Ничего не найдено."
            })

class RestaurantView(ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny, ]
    # queryset = Restaurant.objects.filter(worksFrom__lte=timezone.now()).filter(worksTo__gte=timezone.now())
    serializer_class = RestaurantDetailSerializer

    def get(self, request,*args, **kwargs):
        working = []
        closed = []
        for restaurant in Restaurant.objects.all():
            if restaurant.worksFrom < djangotime.now().time() < restaurant.worksTo:
                working.append(restaurant)
            else:
                closed.append(restaurant)
        # working     = Restaurant.objects.filter(worksFrom__lt=timezone.now().time(), worksTo__gt=timezone.now().time())
        # closed      = Restaurant.objects.filter(worksFrom__gt=timezone.now().time(), worksTo__lt=timezone.now().time())
        openSer     = RestaurantDetailSerializer(working, many=True, context={"request":request})
        closedSer   = RestaurantDetailSerializer(closed, many=True, context={"request": request})
        print('time: ', djangotime.now().time())

        #return self.list(request, *args, **kwargs)
        return Response({
            "open": openSer.data,
            "closed": closedSer.data
        })
        # here gonna be the the query of nearest restaurants

"""
class RestaurantMenuView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request,*args, **kwargs):

        context = {
            'request': request
        }

        queryset = Restaurant.objects.all()
        # restaurant_serializer = RestaurantDetailSerializer(queryset, context=context)
        restaurant_menu_serializer = RestaurantMenuSerializer(queryset, many=True, context=context)

        response = {restaurant_menu_serializer.data}

        # return custom representation of data
        return Response(response)
"""

class RestaurantMenuView(APIView):
    permission_classes = [AllowAny, ]
    queryset = RestaurantMenu.objects.all()
    serializer_class = RestaurantMenuSerializer

    def get(self, request, *args, **kwargs):
        # if 'name' in self.request.GET:
        name = self.request.GET['title']

        menu = RestaurantMenu.objects.filter(restaurant__title=name)

        serializer = RestaurantMenuSerializer(menu, many=True, context={'request': request})

        return Response(serializer.data[0])


class MenuPageView(ListModelMixin, GenericAPIView):

    permission_classes = (AllowAny, )
    serializer_class = CategoryItemsView.serializer_class

    def get(self, request, *args, **kwargs):
        # get objects
        categories = Category.objects.all()
        restaurant = Restaurant.objects.all()

        context = {
                "request": request,
        }

        # get data from serializers
        categories_serializer = CategoryItemsSerializer(categories, many=True, context=context)
        restaurant_serializer = RestaurantDetailSerializer(restaurant, many=True, context=context)

        # customize the response data
        response = {"categories":categories_serializer.data, "restaurant": restaurant_serializer.data[-1]}
        # print('time:', datetime.now().time())

        # return custom representation of data
        return Response(response)


class CartItemAddView(APIView):
    serializer_class = CartItemSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)



    def get(self, request):
        # if user logged in get cart of authorized customer else get cart of unauthorized customer
        # Cart.objects.all().delete()
        # CartItem.objects.all().delete()
        if request.user.is_authenticated:
            print("USER AUTH-D: ", request.user)
            try:
                cart = Cart.objects.get(user=self.request.user)
                print(Cart.objects.filter(user=self.request.user))
            except:
                cart = Cart.objects.create(user=self.request.user)
                cart.save()
        else:
            try:
               cart = Cart.objects.get(device_token=self.request.GET['device_token'])
            except:
                cart = Cart.objects.create(device_token=self.request.GET['device_token'])
                cart.save()
        context = {
            "request": request,
        }
        cartitems = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cartitems, many=True, context=context)
        return Response(serializer.data)


    def post(self, request, pk=None):
        # if user logged in get cart of authorized customer else get cart of unauthorized customer
        if request.user.is_authenticated:
            # print(len(Cart.objects.filter(user=self.request.user)))
            try:
                cart = Cart.objects.get(user=self.request.user)
            except:
                cart = Cart.objects.create(user=self.request.user)
                cart.save()
        else:
            try:
               cart = Cart.objects.get(device_token=request.data['device_token'])
            except:
                cart = Cart.objects.create(device_token=request.data['device_token'])
                cart.save()
        context = {
            "request": request,
        }
        try:
            dish = Dish.objects.get(
                pk=request.data['dish_id']
            )
            quantity = int(request.data.get('quantity'))

        except Exception as e:
            return Response({
                'status': False,
                'detail': "Ошибка при добавлении в корзину"
            })
        try:
            if request.data['additives_id'] != 0:
                additives = DishAdditive.objects.get(
                    id=request.data['additives_id']
                )
            else:
                additives = None
        except:
            additives = None
        try:
            extras_string = request.data.get('extra_id')
        except:
            extras_string = None

        if extras_string is not None:
            extra_list = [int(n) for n in extras_string.split(',')]
        else:
            extra_list = None

        existing_cart_items = CartItem.objects.filter(cart=cart.id, title=dish.title)

        # checking if the adding cart item has a similarity to cart items already added to cart
        # if flag = True the similar cart item  founded and quantity of this item increased
        # if flag = False the similar doesn't founded and creating a new object
        if additives is not None and extra_list is not None:
            flag = False
            for existing_cart_item in existing_cart_items:
                flag = False
                if len(existing_cart_item.additives.all()) == 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) > 0:
                    addtv = existing_cart_item.additives.filter(name=additives)
                    if len(addtv) > 0:
                        flag = True
                    if flag:
                        if len(extra_list) != len(existing_cart_item.extra.all()):
                            flag = False
                            continue
                        else:
                            check = 0
                            for extr in extra_list:
                                flag = False
                                extra = existing_cart_item.extra.filter(id=extr)
                                if extra:
                                    check += 1
                            if check == len(existing_cart_item.extra.all()):
                                flag=True
                if flag == True:
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break

        if additives is None and extra_list is not None:
            flag = False
            for existing_cart_item in existing_cart_items:
                flag = False
                if len(existing_cart_item.additives.all()) > 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) == 0:
                    if len(extra_list) != len(existing_cart_item.extra.all()):
                            flag = False
                    else:
                        check = 0
                        for extr in extra_list:
                            flag = False
                            extra = existing_cart_item.extra.filter(id=extr)
                            if extra:
                                check += 1
                        if check == len(existing_cart_item.extra.all()):
                            flag=True
                if flag == True:
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break

        if additives is not None and extra_list is None:
            flag = False
            for existing_cart_item in existing_cart_items:
                if len(existing_cart_item.additives.all()) == 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) > 0:
                    addtv = existing_cart_item.additives.filter(name=additives)
                    if len(addtv) > 0:
                        flag = True
                    if flag:
                        if len(existing_cart_item.extra.all()) > 0:
                            flag = False
                            continue
                        if len(existing_cart_item.extra.all()) == 0:
                            flag = True
                if flag == True:
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break

        if additives is None and extra_list is None:
            flag = False
            for existing_cart_item in existing_cart_items:
                if len(existing_cart_item.additives.all()) > 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) == 0:
                    if len(existing_cart_item.extra.all()) > 0:
                        flag = False
                    elif len(existing_cart_item.extra.all()) == 0:
                        flag = True

                if flag == True:
                    existing_cart_item.quantity = quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break

        if flag == False:
            img_url = 'http://' + ALLOWED_HOSTS[0] + dish.image.url
            try:
                new_cart_item = CartItem.objects.create(
                        cart=cart,
                        dish_id = dish.id,
                        title=dish.title,
                        price=dish.price,
                        image=img_url,
                        description=dish.description,
                        restaurant=dish.restaurant,
                        portionWeight=dish.portionWeight,
                        quantity = quantity
                )
                new_cart_item.save()
                category = dish.category

                for cat in dish.category.all():#.values():
                    #obj = Category.objects.filter(name=cat["name"])
                    new_cart_item.category.add(cat)
                if additives is not None:
                    new_cart_item.additives.add(additives)
                if extra_list is not None:
                    for extra in extra_list:
                        if extra != 0:
                            obj = DishExtra.objects.get(pk=extra)
                            new_cart_item.extra.add(obj)
                return Response({
                        "status": True
                })
            except  Exception as e:
                print("error:", e)
                return Response({
                    "status": False
                })

class CartItemEditView(APIView):

    def post(self,request,pk=None):

        if request.user.is_authenticated:
            print(len(Cart.objects.filter(user=self.request.user)))
            try:
                cart = Cart.objects.get(user=self.request.user)
            except:
                cart = Cart.objects.create(user=self.request.user)
                cart.save()
        else:
            try:
               cart = Cart.objects.get(device_token=request.data['device_token'])
            except:
                cart = Cart.objects.create(device_token=request.data['device_token'])
                cart.save()
        try:
            cartitem = CartItem.objects.filter(
                pk=request.data['cartitem_id']
            ).filter(cart=cart).first()
            quantity = int(request.data['quantity'])
        except Exception as e:
            print(e)
            return Response({
                'status': False ,
                'detail': "Ошибка запроса при изменении товаров в корзине"
            })
        try:
            additives = DishAdditive.objects.get(
                id=request.data['additives_id']
            )
        except:
            additives = None
        try:
            extras_string = request.data.get('extra_id')
        except:
            extras_string = None

        if extras_string is not None:
            extra_list = [int(n) for n in extras_string.split(',')]
        else:
            extra_list = None

        if cartitem:
            try:
                cartitem.quantity = quantity
                cartitem.save()
                if additives is not None:
                    cartitem.additives.clear()
                    cartitem.additives.add(additives)
                if extra_list is not None:
                    cartitem.extra.clear()
                    for extra in extra_list:
                        obj = DishExtra.objects.get(pk=extra)
                        cartitem.extra.add(obj)
                else:
                    cartitem.extra.clear()
                return Response({
                    "status": True
                })
            except:
                return Response({
                    "status": False
                })
        else:
            return Response({
                "status": False,
                "detail": "Ошибка при изменении"
            })


class CartItemDeleteView(APIView):

    def post(self, request, pk=None):
        if request.user.is_authenticated:
            print(len(Cart.objects.filter(user=self.request.user)))
            try:
                cart = Cart.objects.get(user=self.request.user)
            except:
                cart = Cart.objects.create(user=self.request.user)
                cart.save()
        else:
            try:
               cart = Cart.objects.get(device_token=request.data['device_token'])
            except:
                cart = Cart.objects.create(device_token=request.data['device_token'])
                cart.save()
        try:

            cartitem = CartItem.objects.filter(
                pk=request.data['cartitem_id']
            ).filter(cart=cart)
        except:
            return Response({
                "status": False,
                "detail": "Товар по такому id не найден"
            })
        if cartitem.exists():
            try:
                cartitem.delete()
                return Response({
                    "status": True
                })
            except:
                return Response({
                    "status": False
                })
        else:
            return Response({
                "status": False,
                "detail": "Ошибка при удалении"
            })


class CartDeleteView(APIView):
    def post(self, request,pk=None):
        if request.user.is_authenticated:
            print(len(Cart.objects.filter(user=self.request.user)))
            try:
                cart = Cart.objects.get(user=self.request.user)
            except:
                cart = Cart.objects.create(user=self.request.user)
                cart.save()
        else:
            try:
               cart = Cart.objects.get(device_token=request.data['device_token'])
            except:
                cart = Cart.objects.create(device_token=request.data['device_token'])
                cart.save()
        try:
            CartItem.objects.filter(cart=cart).delete()
            return Response({
                "status": True
            })
        except Exception :
            return ({
                "status": False
            })

class FavoriteRestaurantsView(APIView):
    """
    Class Based View that handles to add restaurant to liked by user

    Args:
        APIView ([class]): [view class from rest framework]
    """
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def get(self, request, *args, **kwargs):
        # if 'search' in self.request.GET:
        # restaurantName = self.request.GET['restaurantName']

        restaurants_qs = Restaurant.objects.filter(likedUsers=self.request.user)

        serializer = RestaurantDetailSerializer(restaurants_qs, many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            restaurant_title = str(request.data['restaurant_title'])
            print(request.method)
        except:
            return Response({
                'status': False,
                'detail': 'Ошибка добавления ресторана в список любимых'
            })

        # user_liked = User.objects.get(pk=self.request.user.id)
        restaurant = Restaurant.objects.get(title=restaurant_title)
        restaurant.likedUsers.add(self.request.user)

        return Response({
            "status": True,
            "detail": "Ресторан добавлен в список любимых"
        })


    def delete(self, request, *args, **kwargs):
        try:
            restaurant_title = self.request.GET['restaurant_title']
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при удалении ресторана из списка любимых."
            })
        restaurant = Restaurant.objects.get(title=restaurant_title)
        restaurant.likedUsers.remove(self.request.user)

        return Response({
            "status": True,
            "detail": "Ресторан удалён из списка любимых"
        })