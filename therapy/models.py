from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


# responsible_person = models.ForeignKey(User, related_name = '',on_delete=models.SET_NULL)
# Вид лучевой терапии
class RadiationTherapyType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Вид лучевой терапии"
        verbose_name_plural = "Виды лучевой терапии"

    def __str__(self):
        str_look = self.name
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Локализация
class Location(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Полное название",
    )
    short_name = models.CharField(
        max_length=100,
        verbose_name="Сокращенное название",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Локализация"
        verbose_name_plural = "Локализации"

    def __str__(self):
        str_look = self.name

        if self.short_name:
            str_look += f" ({self.short_name})"
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Уточненная локализация
class SpecLocation(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Уточненная локализация",
        unique=True,
        blank=False,
        null=False,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name="Локализация",
        blank=False,
        null=False,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Уточненная локализация"
        verbose_name_plural = "Уточненные локализации"

    def __str__(self):
        str_look = self.name
        if self.location:
            str_look += f" ({self.location})"
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Диагноз
class Diagnosis(models.Model):
    code = models.CharField(
        max_length=6, unique=True, blank=False, null=False, verbose_name="Код МКБ-10"
    )
    description = models.TextField(verbose_name="Описание диагноза",blank=False, null=False,)
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Диагноз"
        verbose_name_plural = "Диагнозы"

    def __str__(self):
        str_look = f"{self.code} - {self.description}"
        if self.note:
            str_look += f", {self.note}"
        return str_look


# стадии
class Stage(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name="Название стадии")
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание стадии",
    )

    class Meta:
        verbose_name = "Стадия"
        verbose_name_plural = "Стадии"

    def __str__(self):
        str_look = ""
        if self.name:
            str_look = f"Стадия: {self.name}"
        if self.note:
            str_look += f", Описание: {self.note}"
        return str_look


# группы риска
class RiskGroup(models.Model):
    name = models.TextField(blank=True, null=True, verbose_name="Название риска")
    note = models.TextField(blank=True, null=True, verbose_name="Описание риска")

    class Meta:
        verbose_name = "Риск"
        verbose_name_plural = "Риски"

    def __str__(self):
        str_look = ""
        if self.name:
            str_look = f"Риск: {self.name}"
        if self.note:
            str_look += f", Описание: {self.note}"
        return str_look


# Осложнения
class Complication(models.Model):
    name = models.TextField(
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название осложнения",
    )
    alt_name = models.TextField(
        blank=True,
        null=True,
        verbose_name="Альтернативное название осложнения",
    )
    spec_location = models.ForeignKey(
        SpecLocation,
        on_delete=models.CASCADE,
        verbose_name="Уточненная локализация",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Осложнение"
        verbose_name_plural = "Осложнения"

    def __str__(self):
        str_look = f"Осложнение: {self.name}"
        if self.alt_name:
            str_look += f", Альтернативное название: {self.alt_name}"
        if self.spec_location:
            str_look += f", Локализация: {self.spec_location}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Гистологическая классификация
class Histology(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Гистологическая классификация"
        verbose_name_plural = "Гистологическая классификация"

    def __str__(self):
        str_look = self.name
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Классификация по степени злокачественности (Grade)
class Grade(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Степень злокачественности"
        verbose_name_plural = "Степени злокачественности"

    def __str__(self):
        str_look = self.name
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Система TNM (Tumor, Node, Metastasis)
# Опухоль
class Tumor(models.Model):
    short_name = models.CharField(
        max_length=100,
        verbose_name="Сокращенное название",
        unique=True,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Полное название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Опухоль"
        verbose_name_plural = "Опухоли"

    def __str__(self):
        str_look = self.short_name

        if self.name:
            str_look += f" ({self.name})"
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Узел
class Node(models.Model):
    short_name = models.CharField(
        max_length=100,
        verbose_name="Сокращенное название",
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Полное название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Узлы"
        verbose_name_plural = "Узлы"

    def __str__(self):
        str_look = self.short_name

        if self.name:
            str_look += f" ({self.name})"
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Метастазы
class Metastasis(models.Model):
    short_name = models.CharField(
        max_length=100,
        verbose_name="Сокращенное название",
        blank=True,
        null=True,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Полное название",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Метастазы"
        verbose_name_plural = "Метастазы"

    def __str__(self):
        str_look = self.short_name

        if self.name:
            str_look += f" ({self.name})"
        if self.note:
            str_look += f" {self.note}"
        return str_look


# Клинический случай
class ClinicalCase(models.Model):
    age = models.IntegerField(
        # validators=[MinValueValidator(0)],
        verbose_name="Возраст",
        blank=True,
        null=True,
    )
    age_min = models.IntegerField(
        # validators=[MinValueValidator(0)],
        verbose_name="Минимальный возраст",
        blank=True,
        null=True,
    )
    age_max = models.IntegerField(
        # validators=[MinValueValidator(0)],
        verbose_name="Максимальный возраст",
        blank=True,
        null=True,
    )

    quantity = models.IntegerField(
        # validators=[MinValueValidator(1)],
        default=1,
        verbose_name="Количество",
        blank=False,
        null=False,
    )

    class GenderChoices(models.IntegerChoices):
        male = 1, "Мужской"
        female = 2, "Женский"
        other = 3, "Другой"
        INIT = 0, "Неизвестно"

    gender = models.PositiveSmallIntegerField(
        choices=GenderChoices.choices,
        default=GenderChoices.INIT,
        null=True,
        blank=True,
        verbose_name="Пол",
    )
    diagnosis = models.ForeignKey(
        Diagnosis,
        on_delete=models.SET_NULL,
        verbose_name="МКБ10",
        blank=True,
        null=True,
    )
    refined_diagnosis = models.CharField(
        max_length=255,
        verbose_name="Подробный диагноз",
        blank=True,
        null=True,
    )
    spec_location = models.ForeignKey(
        SpecLocation,
        on_delete=models.CASCADE,
        verbose_name="Уточненная локализация",
        blank=False,
        null=False,
    )
    complication = models.ForeignKey(
        Complication,
        on_delete=models.SET_NULL,
        verbose_name="Осложнение",
        blank=True,
        null=True,
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        verbose_name="Стадия",
        blank=True,
        null=True,
    )
    risk_group = models.ForeignKey(
        RiskGroup,
        on_delete=models.SET_NULL,
        verbose_name="Группа риска",
        blank=True,
        null=True,
    )
    radiation_therapy_type = models.ForeignKey(
        RadiationTherapyType,
        on_delete=models.CASCADE,
        verbose_name="Вид лучевой терапии",
        blank=False,
        null=False,
    )
    tumor = models.ForeignKey(
        Tumor,
        on_delete=models.SET_NULL,
        verbose_name="Опухоль",
        blank=True,
        null=True,
    )
    node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL,
        verbose_name="Узел",
        blank=True,
        null=True,
    )
    metastasis = models.ForeignKey(
        Metastasis,
        on_delete=models.SET_NULL,
        verbose_name="Метастазы",
        blank=True,
        null=True,
    )
    histology = models.ForeignKey(
        Histology,
        on_delete=models.SET_NULL,
        verbose_name="Гистология",
        blank=True,
        null=True,
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        verbose_name="",
        blank=True,
        null=True,
    )
    number_of_fractions = models.IntegerField(
        verbose_name="Количество фракций",
        blank=True,
        null=True,
    )
    single_dose = models.FloatField(
        verbose_name="Разовая очаговая доза",
        blank=True,
        null=True,
    )
    treatment_duration = models.IntegerField(
        verbose_name="Длительность лечения(дней)",
        blank=True,
        null=True,
    )

    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Клинический случай"
        verbose_name_plural = "Клинические случаи"

    def __str__(self):
        str_look = ""

        if self.quantity is not None:
            str_look += f"Количество: {self.quantity}, "
        if self.age is not None:
            str_look += f"Возраст: {self.age}, "
        if self.age_min is not None:
            str_look += f"Минимальный возраст: {self.age_min}, "
        if self.age_max is not None:
            str_look += f"Максимальный возраст: {self.age_max}, "
        if self.gender is not None:
            str_look += f"Пол: {self.get_gender_display()}, "
        if self.diagnosis:
            str_look += f"Диагноз: {self.diagnosis}, "
        if self.refined_diagnosis:
            str_look += f"Подробный диагноз: {self.refined_diagnosis}, "
        if self.spec_location:
            str_look += f"Локализация: {self.spec_location}, "
        if self.complication:
            str_look += f", Осложнение: {self.complication}"
        if self.stage:
            str_look += f", Стадия: {self.stage}"
        if self.risk_group:
            str_look += f", Группа риска: {self.risk_group}"
        if self.radiation_therapy_type:
            str_look += f"Вид терапии: {self.radiation_therapy_type}, "
        if self.histology:
            str_look += f"Гистология: {self.histology}, "
        if self.grade:
            str_look += f"Степень злокачественности: {self.grade}, "
        if self.tumor:
            str_look += f"Опухоль: {self.tumor}, "
        if self.node:
            str_look += f"Узлы: {self.node}, "
        if self.metastasis:
            str_look += f"Метастазы: {self.metastasis}, "
        if self.number_of_fractions is not None:
            str_look += f"Количество фракций: {self.number_of_fractions}, "
        if self.single_dose is not None:
            str_look += f"Разовая доза: {self.single_dose}, "
        if self.treatment_duration is not None:
            str_look += f"Длительность лечения: {self.treatment_duration} дней, "
        if self.note:
            str_look += f"Доп. информация: {self.note}, "

        return str_look[:-2] if str_look else str_look
    


# Единицы измерения
class Unit(models.Model):

    name = models.CharField(
        max_length=50,
        verbose_name="Ед. изм.",
        unique=True,
        blank=True,
        null=True,
    )
    full_name = models.TextField(
        verbose_name="Полное название",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

    def __str__(self):
        str_look = f"Единица измерения: {self.name}"
        if self.full_name:
            str_look += f" ({self.full_name})"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Параметр
class Parameter(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название параметра",
        blank=False,
        null=False,
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Полное название параметра",
        blank=True,
        null=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        verbose_name="Ед. изм.",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Параметр"
        verbose_name_plural = "Параметры"

    def __str__(self):
        str_look = f"Параметр: {self.name}"
        if self.full_name:
            str_look += f", Полное название: {self.full_name}"
        if self.unit:
            str_look += f", Ед. изм.: {self.unit.name}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Модель
class ModelName(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name="Название модели",
        unique=True,
        blank=False,
        null=False,
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Полное название модели",
        blank=True,
        null=True,
    )

    class ModelTypeChoises(models.IntegerChoices):
        TCP = 1, "Tumor Control Probability (TCP)"
        NTCP = 2, "Normal Tissue Complication Probability (NTCP)"
        other = 3, "Другой"
        INIT = 0, "Неизвестно"

    model_type = models.PositiveSmallIntegerField(
        choices=ModelTypeChoises.choices,
        default=ModelTypeChoises.INIT,
        null=False,
        verbose_name="Тип модели",
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"

    def __str__(self):
        str_look = f"Модель: {self.name}"
        if self.full_name:
            str_look += f"({self.full_name})"
        str_look += f", Тип модели: {self.get_model_type_display()}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Структура моделей
class ModelStructure(models.Model):

    model_name = models.ForeignKey(
        ModelName,
        on_delete=models.CASCADE,
        verbose_name="Модель",
        blank=True,
        null=True,
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name="Параметр",
        blank=False,
        null=False,
    )

    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Структура модели"
        verbose_name_plural = "Структуры моделей"

    def __str__(self):
        str_look = f"Структура модели: {self.model_name}, Параметр: {self.parameter}"

        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Результаты измерений
class Result(models.Model):

    model_structure = models.ForeignKey(
        ModelStructure,
        on_delete=models.CASCADE,
        verbose_name="Структура моделей",
        blank=False,
        null=False,
    )
    value = models.FloatField(
        verbose_name="Полученное значение",
        blank=True,
        null=True,
    )
    upper_value = models.FloatField(
        verbose_name="Верхняя граница",
        blank=True,
        null=True,
    )
    lower_value = models.FloatField(
        verbose_name="Нижняя граница",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Результат измерения"
        verbose_name_plural = "Результаты измерений"

    def __str__(self):
        str_look = f"{self.model_structure} Результат: {self.value}, Верхняя граница: {self.upper_value}, Нижняя граница: {self.lower_value}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Источники
class Source(models.Model):

    name = models.TextField(
        verbose_name="Название источника",
        blank=False,
        null=False,
    )
    full_name = models.TextField(
        verbose_name="Полное название источника",
        blank=True,
        null=True,
    )
    url = models.URLField(
        verbose_name="Ссылка на источник",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"

    def __str__(self):
        str_look = f"Источник: {self.name}"
        if self.full_name:
            str_look += f", Полное название: {self.full_name}"
        if self.url:
            str_look += f", Ссылка: {self.url}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look


# Набор данных
class DataSet(models.Model):

    result = models.OneToOneField(
        Result,
        on_delete=models.CASCADE,
        verbose_name="Результат",
        unique=True,
        blank=False,
        null=False,
    )
    сlinical_сase = models.ForeignKey(
        ClinicalCase,
        on_delete=models.CASCADE,
        verbose_name="Клинический случай",
        blank=True,
        null=True,
    )
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        verbose_name="Источник",
        blank=True,
        null=True,
    )
    note = models.TextField(
        blank=True,
        null=True,
        verbose_name="Доп. информация",
    )

    class Meta:
        verbose_name = "Набор данных"
        verbose_name_plural = "Наборы данных"

    def __str__(self):
        str_look = f"Результат: {self.result}"
        if self.сlinical_сase:
            str_look += f", Клинический случай: {self.сlinical_сase}"
        if self.source:
            str_look += f", Источник: {self.source}"
        if self.note:
            str_look += f", Доп. информация: {self.note}"
        return str_look
