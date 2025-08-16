-- Database is already created by docker-compose environment variables
-- Connect to the skillstacker database
\c skillstacker;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    rating DECIMAL(3,2) DEFAULT 0.0,
    reviews_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_id ON orders(product_id);

-- Insert sample data (password is 'password123' for both users)
INSERT INTO users (email, full_name, password_hash, is_admin) VALUES
('admin@skillstacker.com', 'Admin User', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', TRUE),
('user@skillstacker.com', 'Regular User', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', FALSE)
ON CONFLICT (email) DO NOTHING;

INSERT INTO products (name, description, price, category) VALUES
('JavaScript Fundamentals', 'Learn the basics of JavaScript programming', 29.99, 'Programming'),
('React Development', 'Build modern web applications with React', 49.99, 'Web Development'),
('Python for Beginners', 'Start your programming journey with Python', 39.99, 'Programming'),
('Node.js Backend', 'Create powerful backend applications', 59.99, 'Backend'),
('Database Design', 'Master database design principles', 44.99, 'Database'),
('DevOps Essentials', 'Learn modern DevOps practices', 69.99, 'DevOps'),
('Mobile App Development', 'Build mobile apps with React Native', 79.99, 'Mobile'),
('Machine Learning Basics', 'Introduction to ML concepts', 89.99, 'AI/ML'),
('Cloud Computing', 'AWS and cloud fundamentals', 99.99, 'Cloud'),
('Cybersecurity Fundamentals', 'Learn security best practices', 74.99, 'Security')
ON CONFLICT DO NOTHING;