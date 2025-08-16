export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  rating: number;
  reviews_count: number;
  created_at: string;
  updated_at: string;
}

export interface ProductFilters {
  search?: string;
  category?: string;
  minRating?: number;
  page?: number;
  limit?: number;
}

export interface ProductsResponse {
  products: Product[];
  total: number;
  page: number;
  pages: number;
}

export interface Review {
  id: string;
  product_id: number;
  user_id: number;
  rating: number;
  comment: string;
  created_at: string;
  user_name: string;
}