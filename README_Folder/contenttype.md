### ContentType Framework

- 'user X did something' 메세지를 출력하기 위해 X user에 대한 Foreignkey를 이용할 수 있다.

- 하지만 'user X is now following user Y'와 같이 다른 모델(target)을 참조하기 위해 target 모델에 대한 Foreignkey를 추가해야 한다.

  → 일반적인 ForeingKey는 하나의 모델을 연결, 위 예는 하나의 모델이 아닌 다수의 다른 타입의 모델에 연결하기 위함

  → 모델을 추가하지 않고 contenttypes framework를 이용해 프로젝트에 포함된 모든 모델을 추적하거나 모델 간 상호작용이 이뤄지도록 할 수 있다.

  ```
    INSTALLED_APPS = [
    		...
        'django.contrib.contenttypes',
        ...
    ]
  ```

  - Fields of ContentType 

    - app_label: 모델이 속한 응용 프로그램의 이름(from Meta options of model)

    - model: 모델의 이름

    - name: 모델의 human-readable name(verbose_name from Meta options of model)

      ```
        >>> from django.contrib.contenttypes.models import ContentType
        >>> image_type = ContentType.objects.get(app_label='images', model='image')
        >>> image_type
        <ContentType: image>
        >>> image_type.model_class()
        <class 'images.models.Image'>
        >>> from images.models import Image
        >>> ContentType.objects.get_for_model(Image)
        <ContentType: image>
      ```

      - 모델의 관계를 설정하기 위해 아래의 세 가지 필드 설정

        1. content_type: ContentType에 등록된 모델의 Foreignkey 설정: 모델 관계 출력을 위함

        2. object_id: 관계된 객체의 PK(models.PositiveIntegerField) 

           - ContentType에 등록된 모델의 객체 id

        3. content_object: 위 두 필드를 이용한 관계 정의 및 관리 → GenericForeignKey 

           ```python
           class Action(models.Model):
               user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions', db_index=True, on_delete=models.CASCADE)
               verb = models.CharField(max_length=200)
               created = models.DateTimeField(auto_now_add=True)
           
               content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='content_obj',
                                                on_delete=models.CASCADE)
               object_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
               content_object = GenericForeignKey('content_type', 'object_id')
           
               class Meta:
                   ordering = ['-created']
           
           ```

      GenericForeignKey('content_type', 'object_id')

      - 첫 번째 인수(content_type): ContentType에 등록되어있는 현재 동작을 실행하는  모델
      - 두 번째 인수(object_id): ContentType에 등록되어있는 대상(동작하고자 하는) 모델
      - 두 인수는 모두 ContentType에 포함된 ForeignKey이어야 한다.

      **Generic Relation**

      [The contenttypes framework | Django documentation | Django](https://docs.djangoproject.com/en/2.2/ref/contrib/contenttypes/#generic-relations)

      

      