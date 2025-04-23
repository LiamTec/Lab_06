from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Reporter, Article, Tag

# Registrar el modelo Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuración del admin para las categorías"""
    list_display = ("name", "slug", "article_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    
    def article_count(self, obj):
        """Contar artículos en esta categoría"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Artículos"

# Inline para las etiquetas en el artículo
class TagInline(admin.TabularInline):
    """Admin en línea para las etiquetas"""
    model = Tag.articles.through
    extra = 1

# Registrar el modelo Reporter
@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    """Configuración del admin para los reporteros"""
    list_display = ("display_name", "article_count")
    search_fields = ("user__username", "user__first_name", "user__last_name", "bio")

    def display_name(self, obj):
        """Mostrar el nombre completo del reportero"""
        return obj.user.get_full_name() or obj.user.username
    display_name.short_description = "Nombre"

    def article_count(self, obj):
        """Contar artículos por este reportero"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Artículos"

# Registrar el modelo Article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Configuración del admin para los artículos"""
    list_display = ("title", "reporter", "category", "status", "published_date", "display_image")
    list_filter = ("status", "category", "published_date", "reporter")
    search_fields = ("title", "content", "reporter__user__username")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    inlines = [TagInline]
    
    fieldsets = (
        ("Contenido", {
            "fields": ("title", "slug", "content", "summary", "image")
        }),
        ("Publicación", {
            "fields": ("status", "category", "reporter")
        }),
    )

    def display_image(self, obj):
        """Mostrar la imagen del artículo"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No hay imagen"
    display_image.short_description = "Imagen"

# Registrar el modelo Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Configuración del admin para las etiquetas"""
    list_display = ("name", "slug", "article_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    
    def article_count(self, obj):
        """Contar artículos con esta etiqueta"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Artículos"
