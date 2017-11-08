from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.models import Role, User
from snippets.serializers import RoleSerializer, UserSerializer
from rest_framework import generics
import logging
from django.http import Http404

log = logging.getLogger("MYAPP")


def print_sql(queryset):
    print (queryset.query.get_compiler('default').as_sql())


# class RoleList(generics.ListCreateAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     print_sql(queryset)
#
#     def perform_create(self, serializer):
#         print ('---1--> perform_create ', self, serializer)
#
#
# class RoleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Role.objects.all()
#     serializer_class = RoleSerializer
#     print_sql(queryset)
#
#     def perform_create(self, serializer):
#         print ('---2--> perform_create ', self, serializer)


# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     print_sql(queryset)
#
#     # def perform_create(self, serializer):
#     #     print ('---3--> perform_create ', self.request)
#     #     serializer.save(role=self.request.role)
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     print_sql(queryset)
#
#     def perform_create(self, serializer):
#         print ('---4--> perform_create ', self, serializer)
#         # serializer.save(owner=self.request.user)

#########

@api_view(['GET', 'POST'])
def user_list(request, format=None):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        role_id = request.data['role_id']
        try:
            role = Role.objects.get(pk=role_id)
        except Role.DoesNotExist:
            return Response('Role(%s) does not exist' % role_id, status=status.HTTP_404_NOT_FOUND)

        print ('-----444---> ', request.data);
        # role = Role.objects.get("1")
        # print ('-----55---> ', role);
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print ('====> BEFORE save ', serializer, request);
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#########

@api_view(['GET', 'POST'])
def role_list(request, format=None):
    """
    List all code roles, or create a new role.
    """
    if request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def role_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code role.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # from django.http import HttpResponse, JsonResponse
        # from django.views.decorators.csrf import csrf_exempt
        # from rest_framework.renderers import JSONRenderer
        # from rest_framework.parsers import JSONParser
        # from snippets.models import Snippet
        # from snippets.serializers import SnippetSerializer
        #
        # @csrf_exempt
        # def snippet_list(request):
        #     """
        #     List all code snippets, or create a new snippet.
        #     """
        #     if request.method == 'GET':
        #         snippets = Snippet.objects.all()
        #         serializer = SnippetSerializer(snippets, many=True)
        #         return JsonResponse(serializer.data, safe=False)
        #
        #     elif request.method == 'POST':
        #         data = JSONParser().parse(request)
        #         serializer = SnippetSerializer(data=data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return JsonResponse(serializer.data, status=201)
        #         return JsonResponse(serializer.errors, status=400)
        #
        # @csrf_exempt
        # def snippet_detail(request, pk):
        #     """
        #     Retrieve, update or delete a code snippet.
        #     """
        #     try:
        #         snippet = Snippet.objects.get(pk=pk)
        #     except Snippet.DoesNotExist:
        #         return HttpResponse(status=404)
        #
        #     if request.method == 'GET':
        #         serializer = SnippetSerializer(snippet)
        #         return JsonResponse(serializer.data)
        #
        #     elif request.method == 'PUT':
        #         data = JSONParser().parse(request)
        #         serializer = SnippetSerializer(snippet, data=data)
        #         if serializer.is_valid():
        #             serializer.save()
        #             return JsonResponse(serializer.data)
        #         return JsonResponse(serializer.errors, status=400)
        #
        #     elif request.method == 'DELETE':
        #         snippet.delete()
        #         return HttpResponse(status=204)
