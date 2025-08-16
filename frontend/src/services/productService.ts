import { api } from '@/lib/api';
import { Product, ProductFilters, ProductsResponse, Review } from '@/types/product';

class ProductService {
  async getProducts(filters: ProductFilters = {}): Promise<ProductsResponse> {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        const paramKey = key === 'minRating' ? 'min_rating' : key;
        params.append(paramKey, value.toString());
      }
    });

    const response = await api.get(`/products?${params.toString()}`);
    return response.data;
  }

  async getProduct(id: number): Promise<Product> {
    const response = await api.get(`/products/${id}`);
    return response.data;
  }

  async getCategories(): Promise<string[]> {
    const response = await api.get('/products/categories');
    return response.data;
  }

  async getProductReviews(productId: number): Promise<Review[]> {
    const response = await api.get(`/products/${productId}/reviews`);
    return response.data;
  }

  async createReview(productId: number, rating: number, comment: string): Promise<Review> {
    const response = await api.post(`/products/${productId}/reviews`, {
      rating,
      comment
    });
    return response.data;
  }
}

export const productService = new ProductService();