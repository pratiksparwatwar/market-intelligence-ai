import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: API_URL });

export interface Article {
  id: number;
  title: string;
  source: string;
  url: string;
  published_at: string | null;
  summary: string | null;
  asset_tags: string[];
  sector_tags: string[];
  macro_tags: string[];
  created_at: string;
}

export interface MarketTheme {
  id: number;
  theme_title: string;
  short_summary: string;
  why_it_matters: string;
  affected_assets: string[];
  affected_sectors: string[];
  sentiment: "bullish" | "bearish" | "neutral" | "mixed";
  confidence_score: number;
  risk_level: "low" | "medium" | "high";
  supporting_article_ids: number[];
  generated_at: string;
}

export interface MarketThemeDetail extends MarketTheme {
  supporting_articles: Article[];
}

export interface AssetSummary {
  asset: string;
  theme_count: number;
  article_count: number;
  latest_sentiment: string | null;
}

export const fetchThemes = (params?: Record<string, string>) =>
  api.get<MarketTheme[]>("/api/themes", { params }).then((r) => r.data);

export const fetchTheme = (id: number) =>
  api.get<MarketThemeDetail>(`/api/themes/${id}`).then((r) => r.data);

export const fetchArticles = (params?: Record<string, string>) =>
  api.get<Article[]>("/api/articles", { params }).then((r) => r.data);

export const fetchAssets = () =>
  api.get<AssetSummary[]>("/api/assets").then((r) => r.data);

export const fetchAssetThemes = (asset: string) =>
  api.get<MarketTheme[]>(`/api/assets/${encodeURIComponent(asset)}/themes`).then((r) => r.data);

export const fetchAssetArticles = (asset: string) =>
  api.get<Article[]>(`/api/assets/${encodeURIComponent(asset)}/articles`).then((r) => r.data);

export const adminFetchNews = () =>
  api.post("/api/admin/fetch-news").then((r) => r.data);

export const adminGenerateThemes = () =>
  api.post("/api/admin/generate-themes").then((r) => r.data);

export const adminClearData = () =>
  api.delete("/api/admin/clear-data").then((r) => r.data);
