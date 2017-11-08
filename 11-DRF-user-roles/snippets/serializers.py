from rest_framework.serializers import ModelSerializer
from snippets.models import Snippet, Role, User, LANGUAGE_CHOICES, STYLE_CHOICES

class UserSerializer(ModelSerializer):
    # email = serializers.EmailField()
    # content = serializers.CharField(max_length=200)
    # created = serializers.DateTimeField()
    # role_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        print ('----> UserSerializer.created', self, '\n', self.initial_data,
               '\n', validated_data)
        role_id = self.initial_data['role_id'] # TODO better way ?
        print ('---- 555 ----> ', role_id);
        # role = Role.objects.get(id=role_id)
        role = Role.objects.get(pk=role_id)
        return User.objects.create(role=role, **validated_data)

    class Meta:
        model = User
        # model.role = Role
        fields = ('id', 'role_id', 'first_name', 'last_name', 'email', 'created_at')


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class SnippetSerializer(ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')


        # class SnippetSerializer(serializers.Serializer):
        #     id = serializers.IntegerField(read_only=True)
        #     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
        #     code = serializers.CharField(style={'base_template': 'textarea.html'})
        #     linenos = serializers.BooleanField(required=False)
        #     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
        #     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
        #
        #     def create(self, validated_data):
        #         """
        #         Create and return a new `Snippet` instance, given the validated data.
        #         """
        #         return Snippet.objects.create(**validated_data)
        #
        #     def update(self, instance, validated_data):
        #         """
        #         Update and return an existing `Snippet` instance, given the validated data.
        #         """
        #         instance.title = validated_data.get('title', instance.title)
        #         instance.code = validated_data.get('code', instance.code)
        #         instance.linenos = validated_data.get('linenos', instance.linenos)
        #         instance.language = validated_data.get('language', instance.language)
        #         instance.style = validated_data.get('style', instance.style)
        #         instance.save()
        #         return instance
