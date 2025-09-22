# Prasanth S Portfolio Website

A modern, responsive portfolio website built with Flask, featuring a blog system and admin panel.

## Features

- **Responsive Design**: Modern, mobile-first design that looks great on all devices
- **Portfolio Sections**: Home, About, Projects, Skills, Contact
- **Blog System**: Separate blog section with full CRUD functionality
- **Admin Panel**: Secure admin interface for managing blog posts and viewing contact messages
- **Contact Form**: Functional contact form with database storage
- **Modern UI**: Clean, professional design with smooth animations

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite (with schema auto-creation)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with custom design system
- **Security**: Password hashing, session management

## Quick Start

### 1. Clone/Extract the project
```bash
# If you have the zip file, extract it
# Or if cloning from repository:
git clone <repository-url>
cd prasanth_portfolio
```

### 2. Create virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your profile image (optional)
Place your profile photo at `static/images/profile.jpg`

### 5. Run the application
```bash
python app.py
```

### 6. Access the website
- **Portfolio**: http://localhost:5000
- **Blog**: http://localhost:5000/blogs
- **Admin**: http://localhost:5000/admin/login

## Default Admin Credentials

- **Email**: prasanth_2003@outlook.com
- **Password**: admin123

**⚠️ Important**: Change the admin password immediately after first login!

## File Structure

```
prasanth_portfolio/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── instance/             
│   └── portfolio.db      # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css     # Modern CSS styles
│   ├── js/
│   │   └── app.js        # Interactive JavaScript
│   └── images/
│       └── profile.jpg   # Your profile photo
├── templates/
│   ├── index.html        # Main portfolio page
│   ├── blogs.html        # Blog listing page
│   ├── blog_detail.html  # Individual blog post page
│   ├── admin_login.html  # Admin login form
│   ├── admin_dashboard.html   # Admin dashboard
│   └── admin_blog_form.html   # Blog create/edit form
└── README.md
```

## Key Features

### Portfolio Sections
- **Hero Section**: Professional introduction with profile photo
- **About Section**: Education, experience, and achievements
- **Projects Section**: Featured projects with technology tags
- **Skills Section**: Technical skills organized by category
- **Certifications**: Professional certifications display
- **Contact Section**: Contact form and social links

### Blog System
- **Public Blog**: Visitors can read published blog posts
- **Admin Interface**: Create, edit, delete, and manage blog posts
- **Rich Content**: HTML support for formatted blog posts
- **Search**: Client-side search functionality for blog posts
- **Responsive**: Mobile-friendly blog layout

### Admin Features
- **Secure Login**: Password-based authentication
- **Dashboard**: Overview of blog posts and contact messages
- **Blog Management**: Full CRUD operations for blog posts
- **Contact Messages**: View submitted contact form messages
- **Draft/Publish**: Control post visibility

## Customization

### Updating Personal Information
Edit the `portfolio_data` dictionary in `app.py`:
```python
portfolio_data = {
    'personal_info': {
        'name': 'Your Name',
        'title': 'Your Title',
        'email': 'your.email@example.com',
        # ... other details
    }
    # ... other sections
}
```

### Styling
- Modify `static/css/style.css` for design changes
- CSS uses a modern design system with CSS variables
- Responsive design with mobile-first approach

### Adding New Sections
1. Update the `portfolio_data` in `app.py`
2. Modify `templates/index.html` to display new content
3. Add navigation links if needed

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set environment variables:
   ```bash
   export FLASK_ENV=production
   ```
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

### Database
- SQLite database is automatically created on first run
- Database file: `instance/portfolio.db`
- Schema includes: admin, blog_posts, contact_messages

## Security Notes

1. **Change default admin password** immediately after setup
2. **Set strong secret key** for production (in `app.py`)
3. **Use HTTPS** in production
4. **Regular backups** of the SQLite database

## Browser Support

- Chrome (latest)
- Firefox (latest)  
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, contact Prasanth S at prasanth_2003@outlook.com

---

Built with ❤️ using Flask and modern web technologies.
