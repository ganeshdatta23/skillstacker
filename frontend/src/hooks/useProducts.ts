import { useState, useEffect, useCallback } from 'react';
import { productService } from '@/services/productService';
import { Product, ProductFilters, ProductsResponse } from '@/types/product';

interface UseProductsReturn {
  products: Product[];
  loading: boolean;
  error: string | null;
  total: number;
  page: number;
  pages: number;
  refetch: (filters?: ProductFilters) => Promise<void>;
}

export const useProducts = (initialFilters: ProductFilters = {}): UseProductsReturn => {
  const [data, setData] = useState<ProductsResponse>({
    products: [],
    total: 0,
    page: 1,
    pages: 1
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = useCallback(async (filters: ProductFilters = initialFilters) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await productService.getProducts(filters);
      setData(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch products');
    } finally {
      setLoading(false);
    }
  }, [initialFilters]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  return {
    products: data.products,
    total: data.total,
    page: data.page,
    pages: data.pages,
    loading,
    error,
    refetch: fetchProducts
  };
};