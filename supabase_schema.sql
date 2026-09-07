CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    content JSONB NOT NULL,
    seo_title TEXT,
    seo_description TEXT,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES admins(id),
    updated_by INTEGER REFERENCES admins(id),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE blogs (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    excerpt TEXT,
    content TEXT NOT NULL,
    featured_image TEXT,
    image_alt TEXT,
    author TEXT,
    category TEXT,
    tags TEXT,
    status TEXT DEFAULT 'draft',
    seo_title TEXT,
    seo_description TEXT,
    og_image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES admins(id),
    updated_by INTEGER REFERENCES admins(id),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    short_description TEXT,
    hero_content JSONB,
    images JSONB,
    technologies JSONB,
    features JSONB,
    benefits JSONB,
    process_steps JSONB,
    statistics JSONB,
    faqs JSONB,
    cta JSONB,
    related_case_studies JSONB,
    seo_title TEXT,
    seo_description TEXT,
    display_order INTEGER DEFAULT 0,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES admins(id),
    updated_by INTEGER REFERENCES admins(id),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE case_studies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    client TEXT,
    industry TEXT,
    related_service TEXT,
    overview TEXT,
    challenge TEXT,
    solution TEXT,
    process JSONB,
    technologies JSONB,
    images JSONB,
    results JSONB,
    metrics JSONB,
    testimonial JSONB,
    cta JSONB,
    seo_title TEXT,
    seo_description TEXT,
    display_order INTEGER DEFAULT 0,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE,
    created_by INTEGER REFERENCES admins(id),
    updated_by INTEGER REFERENCES admins(id),
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE contact_submissions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT DEFAULT 'new',
    internal_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    alt_text TEXT,
    size INTEGER,
    mime_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    uploaded_by INTEGER REFERENCES admins(id)
);
