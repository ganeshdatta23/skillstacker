// MongoDB initialization script
db = db.getSiblingDB('skillstacker');

// Create reviews collection with sample data
db.reviews.insertMany([
  {
    product_id: 1,
    user_id: 2,
    rating: 5,
    title: "Excellent course!",
    content: "This JavaScript course is fantastic. Clear explanations and great examples.",
    created_at: new Date(),
    updated_at: new Date(),
    helpful_count: 12
  },
  {
    product_id: 1,
    user_id: 1,
    rating: 4,
    title: "Good for beginners",
    content: "Perfect for someone starting with JavaScript. Well structured content.",
    created_at: new Date(),
    updated_at: new Date(),
    helpful_count: 8
  },
  {
    product_id: 2,
    user_id: 2,
    rating: 5,
    title: "React mastery",
    content: "Comprehensive React course with modern practices and hooks.",
    created_at: new Date(),
    updated_at: new Date(),
    helpful_count: 15
  },
  {
    product_id: 3,
    user_id: 1,
    rating: 4,
    title: "Great Python intro",
    content: "Solid foundation in Python programming. Recommended!",
    created_at: new Date(),
    updated_at: new Date(),
    helpful_count: 6
  }
]);

// Create indexes
db.reviews.createIndex({ "product_id": 1 });
db.reviews.createIndex({ "user_id": 1 });
db.reviews.createIndex({ "rating": 1 });
db.reviews.createIndex({ "created_at": -1 });

print("MongoDB initialized with sample reviews data");