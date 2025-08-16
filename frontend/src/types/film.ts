export interface Film {
  film_id: number;
  title: string;
  description?: string;
  release_year?: number;
  rental_rate: string;
  length?: number;
  rating?: string;
}

export interface Actor {
  actor_id: number;
  first_name: string;
  last_name: string;
}

export interface Category {
  category_id: number;
  name: string;
}

export interface Publication {
  _id?: string;
  id?: string;
  title: string;
  content?: string;
  related_title?: string;
  type: string;
  groups: string[];
  subgroups?: string[];
  author?: string;
}

export interface DataOverview {
  postgresql: {
    films: { total: number; sample_titles: string[] };
    actors: { total: number; sample_names: string[] };
    categories: { total: number; all_categories: string[] };
    customers: { total: number; sample_emails: string[] };
    rentals: { total: number };
    payments: { total: number };
  };
  mongodb: {
    publications: { total: number; sample_titles: string[] };
  };
  summary: {
    total_films: number;
    total_actors: number;
    total_categories: number;
    total_customers: number;
    total_rentals: number;
    total_payments: number;
    total_publications: number;
  };
}