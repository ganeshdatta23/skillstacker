import { api } from '@/lib/api';
import { Film, Actor, Category, Publication, DataOverview } from '@/types/film';

export const dataService = {
  // Films
  async getAllFilms(): Promise<Film[]> {
    const response = await api.get('/films/all');
    return response.data;
  },

  async getFilms(params?: {
    search?: string;
    rating?: string;
    min_year?: number;
    max_year?: number;
    limit?: number;
  }): Promise<Film[]> {
    const response = await api.get('/films/', { params });
    return response.data;
  },

  async getFilmStats() {
    const response = await api.get('/films/stats');
    return response.data;
  },

  async getFilm(filmId: number): Promise<Film> {
    const response = await api.get(`/films/${filmId}`);
    return response.data;
  },

  // Actors
  async getAllActors(): Promise<Actor[]> {
    const response = await api.get('/actors/all');
    return response.data;
  },

  async getActors(params?: {
    search?: string;
    limit?: number;
  }): Promise<Actor[]> {
    const response = await api.get('/actors/', { params });
    return response.data;
  },

  async getActorStats() {
    const response = await api.get('/actors/stats');
    return response.data;
  },

  async getActor(actorId: number): Promise<Actor> {
    const response = await api.get(`/actors/${actorId}`);
    return response.data;
  },

  // Categories
  async getAllCategories(): Promise<Category[]> {
    const response = await api.get('/categories/all');
    return response.data;
  },

  async getCategories(): Promise<Category[]> {
    const response = await api.get('/categories/');
    return response.data;
  },

  async getCategoryStats() {
    const response = await api.get('/categories/stats');
    return response.data;
  },

  async getCategory(categoryId: number): Promise<Category> {
    const response = await api.get(`/categories/${categoryId}`);
    return response.data;
  },

  // Products (Films alias)
  async getAllProducts(): Promise<Film[]> {
    const response = await api.get('/products/all');
    return response.data;
  },

  async getProducts(params?: {
    search?: string;
    category?: string;
    min_rating?: number;
    limit?: number;
  }): Promise<Film[]> {
    const response = await api.get('/products/', { params });
    return response.data;
  },

  async getProductStats() {
    const response = await api.get('/products/stats');
    return response.data;
  },

  async getProductCategories() {
    const response = await api.get('/products/categories');
    return response.data;
  },

  async getProduct(productId: number): Promise<Film> {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  // Publications
  async getPublications(params?: {
    search?: string;
    limit?: number;
  }): Promise<{ publications: Publication[] }> {
    const searchParams = new URLSearchParams();
    // Use a default search term if none provided
    const searchTerm = params?.search || 'a';
    searchParams.append('q', searchTerm);
    searchParams.append('category', 'publications');
    
    if (params?.limit) {
      searchParams.append('limit', params.limit.toString());
    }
    
    const response = await api.get(`/unified/search?${searchParams.toString()}`);
    return { publications: response.data.publications || [] };
  },

  async getPublicationStats() {
    const response = await api.get('/unified/stats');
    return {
      total_publications: response.data.mongodb?.publications || 0
    };
  }
};