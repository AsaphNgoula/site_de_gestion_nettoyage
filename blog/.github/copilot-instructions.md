# ProClean Django Site - AI Coding Guide

## Architecture Overview

**Project Type**: Django 4.0 web application for a cleaning services company (NG Conciergerie)

**Key Components**:

- **proclean** app: Main business logic (models, views, forms)
- **blog** project: Django project configuration and URL routing
- **templates/**: HTML with Tailwind CSS via django-compressor
- **static/**: CSS (Tailwind), JS (Flowbite), compiled assets

**Data Flow**:

1. Request enters via `blog/urls.py` → routed to `proclean/urls.py`
2. View in `proclean/views.py` processes request, queries `proclean/models.py`
3. Template renders with context, uses media files from `/media/` directory
4. Emails sent via `send_mail()` using SMTP (configured in settings.py via `.env`)

## Core Models Pattern

Located in `proclean/models.py`:

```python
# Example: ContactMessage model demonstrates pattern
- Uses descriptive verbose_name in French
- Implements __str__() for admin display
- Custom methods for business logic (e.g., mark_as_read(), nom_complet property)
- Proper Meta class with ordering, verbose_name_plural
- Optional fields use blank=True, null=True
```

**Key Models**:

- `Service`: Services with image uploads to `services/` folder
- `CarouselImage`: Homepage carousel, toggled by `is_active`
- `ContactMessage`: Contact form submissions (read tracking via `lu` field)
- `JobApplication`: Job applications with file uploads, region/availability choices

## Critical Development Workflows

### Environment Setup

```bash
cd /home/asaph/Documents/site_gestion_netoyage/blog
source .venv/bin/activate
```

### Configuration (`.env` required)

```
SECRET_KEY=<django-secret>
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=asaphngoula237@gmail.com
EMAIL_HOST_PASSWORD=<app-password>
EMAIL_USE_TLS=True
```

### Database

- **Engine**: PostgreSQL (psycopg2 driver)
- **Credentials in settings.py**: pproclean user, hardcoded password (⚠️ security concern)
- **Migrations**: Standard Django (`python manage.py migrate`)

### CSS/JS Build (Tailwind)

```bash
npm run dev          # Watch mode for development
npm run build        # Production build (cleans and rebuilds CSS)
```

After CSS changes, Django's compressor (enabled in settings) caches compiled assets in `static/CACHE/`.

### Running Development Server

```bash
python manage.py runserver
```

## Project-Specific Conventions

### URL Naming Pattern

URLs in `proclean/urls.py` use clear slugs for service details:

```
/services/nettoyage-profond/  → nettoyage_profondeur_detail view
/services/nettoyage-tapis/    → nettoyage_tapis_detail view
```

When adding new service pages, follow this `services/<slug>/` pattern.

### Email Handling

**Pattern in views.py (send_message function)**:

- Always use `send_mail()` from Django, not `EmailMultiAlternatives` initially (simpler, more reliable)
- Email config uses environment variables via `python-decouple` (`config()` function)
- Emails sent to admin (`EMAIL_HOST_USER`) and confirmation to user's email
- All emails catch exceptions and fall back gracefully with user messages

### Admin Customization

Located in `proclean/admin.py`:

- Use `@admin.register()` decorator with `ModelAdmin` subclass
- Implement `list_display`, `list_filter`, `search_fields` for usability
- Add `readonly_fields`, `fieldsets`, custom `actions` for admin UI
- Example: ContactMessage admin has date_hierarchy, custom display methods

### Media File Organization

```
media/
  carousel/       # Homepage carousel images
  services/       # Service detail images
  cv_applications/# Job application CVs (organized by date: 2025/12/...)
  images/         # General images
```

Settings: `MEDIA_URL = "/media/"`, `MEDIA_ROOT = BASE_DIR / "media"`

### Template Structure

- Base template: `_base.html`
- Home page: `accueil.html` (carousel, service cards)
- Service detail templates: `detail_services/detail_<service>.html`
- Reusable email templates: `email/` directory

## Integration Points & Dependencies

### External Services

- **Email**: Gmail SMTP (configured via `.env`)
- **File Storage**: Local filesystem (`media/` folder)
- **Image Processing**: Pillow (for image uploads)

### Third-Party Packages

- `django-compressor`: CSS/JS compression and caching
- `pillow`: Image uploads in models
- `psycopg2`: PostgreSQL database driver
- `python-decouple`: Environment variable management

### Asset Pipeline

- **CSS**: Tailwind CLI compiles `static/src/input.css` → `static/src/output.css`
- **django-compressor**: Minifies and caches in `static/CACHE/` (enabled in settings)
- **JS**: Flowbite pre-compiled `js/flowbite.min.js`

## Common Tasks

**Adding a new service detail page**:

1. Create template: `templates/detail_services/detail_<service>.html`
2. Add view function in `proclean/views.py` (e.g., `nettoyage_tapis_detail()`)
3. Register URL in `proclean/urls.py` with pattern `/services/<slug>/`
4. Add service image to `media/services/`

**Adding form validation**:

- Extend `JobApplicationForm` in `proclean/forms.py` with custom `clean_*()` methods
- Model forms use `Meta.model` and `Meta.fields` pattern

**Debugging email issues**:

- Check `.env` has correct Gmail app password (not regular password)
- Verify `EMAIL_USE_TLS=True` in settings
- Test with simple `send_mail()` before complex `EmailMultiAlternatives`
- Console logs show email flow (search "✅" and "❌" in views.py)

## Important Notes

⚠️ **Security Issues** (address before production):

- PostgreSQL password hardcoded in `settings.py` (move to `.env`)
- DEBUG = True in settings (should be environment-dependent)
- `ALLOWED_HOSTS` is empty (set to actual domain)

⚠️ **Current Limitations**:

- Service data partially hardcoded in `home()` view (list of dicts)
- No caching implemented despite django-compressor enabled
- File uploads lack virus scanning

---

**Last Updated**: December 26, 2025  
**Django Version**: 4.0 | **Python**: 3.12+ | **Database**: PostgreSQL
