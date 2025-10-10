/*
  # Create Initial Schema for Marketing Dashboard

  ## Overview
  This migration sets up the complete database schema for the SaaS ERP Marketing Dashboard system.

  ## 1. New Tables
  
  ### `companies`
  - `id` (uuid, primary key) - Unique company identifier
  - `name` (text) - Company name
  - `created_at` (timestamptz) - Registration timestamp
  - `updated_at` (timestamptz) - Last update timestamp
  
  ### `monthly_metrics`
  - `id` (uuid, primary key) - Unique metric record identifier
  - `company_id` (uuid, foreign key) - Links to companies table
  - `month` (text) - Month in format 'MMM/YY' (e.g., 'Jan/25')
  - `year` (integer) - Year (e.g., 2025)
  - `month_number` (integer) - Month number (1-12) for sorting
  - `sessions` (integer) - Total website sessions
  - `first_visits` (integer) - First-time visitors
  - `leads` (integer) - Total leads generated
  - `tc_users` (numeric) - Conversion rate users to leads (%)
  - `web_clients` (integer) - Clients acquired through web
  - `tc_leads` (numeric) - Conversion rate leads to sales (%)
  - `web_revenue` (numeric) - Revenue from web channel
  - `avg_ticket` (numeric) - Average ticket value
  - `meta_cost` (numeric) - Meta Ads investment
  - `google_cost` (numeric) - Google Ads investment
  - `total_ads` (numeric) - Total advertising spend
  - `cac` (numeric) - Customer Acquisition Cost
  - `ltv` (numeric) - Lifetime Value
  - `cac_ltv_ratio` (numeric) - CAC to LTV ratio
  - `roi` (numeric) - Return on Investment (%)
  - `created_at` (timestamptz) - Record creation timestamp
  - `updated_at` (timestamptz) - Last update timestamp
  
  ### `benchmarks`
  - `id` (uuid, primary key) - Unique benchmark identifier
  - `metric_name` (text) - Name of the metric
  - `min_value` (numeric) - Minimum acceptable value
  - `max_value` (numeric) - Maximum acceptable value
  - `ideal_value` (numeric) - Ideal/target value
  - `critical_value` (numeric, nullable) - Critical threshold value
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### `pricing_plans`
  - `id` (uuid, primary key) - Unique plan identifier
  - `name` (text) - Plan name
  - `price` (numeric) - Monthly price
  - `created_at` (timestamptz) - Record creation timestamp
  
  ### `extensions`
  - `id` (uuid, primary key) - Unique extension identifier
  - `name` (text) - Extension name
  - `price` (numeric) - Monthly price
  - `created_at` (timestamptz) - Record creation timestamp

  ## 2. Security
  - Enable Row Level Security (RLS) on all tables
  - Users can only access data from their own company
  - Authenticated users required for all operations

  ## 3. Important Notes
  - All monetary values stored with 2 decimal precision
  - Timestamps use UTC timezone
  - Unique constraint on company_id + month + year for metrics to prevent duplicates
*/

-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create monthly_metrics table
CREATE TABLE IF NOT EXISTS monthly_metrics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  month text NOT NULL,
  year integer NOT NULL,
  month_number integer NOT NULL CHECK (month_number >= 1 AND month_number <= 12),
  sessions integer DEFAULT 0,
  first_visits integer DEFAULT 0,
  leads integer DEFAULT 0,
  tc_users numeric(5,2) DEFAULT 0,
  web_clients integer DEFAULT 0,
  tc_leads numeric(5,2) DEFAULT 0,
  web_revenue numeric(10,2) DEFAULT 0,
  avg_ticket numeric(10,2) DEFAULT 0,
  meta_cost numeric(10,2) DEFAULT 0,
  google_cost numeric(10,2) DEFAULT 0,
  total_ads numeric(10,2) DEFAULT 0,
  cac numeric(10,2) DEFAULT 0,
  ltv numeric(10,2) DEFAULT 0,
  cac_ltv_ratio numeric(5,2) DEFAULT 0,
  roi numeric(10,2) DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(company_id, month, year)
);

-- Create benchmarks table
CREATE TABLE IF NOT EXISTS benchmarks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  metric_name text UNIQUE NOT NULL,
  min_value numeric(10,2) NOT NULL,
  max_value numeric(10,2) NOT NULL,
  ideal_value numeric(10,2) NOT NULL,
  critical_value numeric(10,2),
  created_at timestamptz DEFAULT now()
);

-- Create pricing_plans table
CREATE TABLE IF NOT EXISTS pricing_plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text UNIQUE NOT NULL,
  price numeric(10,2) NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create extensions table
CREATE TABLE IF NOT EXISTS extensions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text UNIQUE NOT NULL,
  price numeric(10,2) NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_monthly_metrics_company_id ON monthly_metrics(company_id);
CREATE INDEX IF NOT EXISTS idx_monthly_metrics_year_month ON monthly_metrics(year, month_number);

-- Enable Row Level Security
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE benchmarks ENABLE ROW LEVEL SECURITY;
ALTER TABLE pricing_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE extensions ENABLE ROW LEVEL SECURITY;

-- RLS Policies for companies table
CREATE POLICY "Users can view own company"
  ON companies FOR SELECT
  TO authenticated
  USING (auth.uid()::text = (auth.jwt()->>'company_id'));

CREATE POLICY "Users can update own company"
  ON companies FOR UPDATE
  TO authenticated
  USING (auth.uid()::text = (auth.jwt()->>'company_id'))
  WITH CHECK (auth.uid()::text = (auth.jwt()->>'company_id'));

-- RLS Policies for monthly_metrics table
CREATE POLICY "Users can view own company metrics"
  ON monthly_metrics FOR SELECT
  TO authenticated
  USING (company_id::text = (auth.jwt()->>'company_id'));

CREATE POLICY "Users can insert own company metrics"
  ON monthly_metrics FOR INSERT
  TO authenticated
  WITH CHECK (company_id::text = (auth.jwt()->>'company_id'));

CREATE POLICY "Users can update own company metrics"
  ON monthly_metrics FOR UPDATE
  TO authenticated
  USING (company_id::text = (auth.jwt()->>'company_id'))
  WITH CHECK (company_id::text = (auth.jwt()->>'company_id'));

CREATE POLICY "Users can delete own company metrics"
  ON monthly_metrics FOR DELETE
  TO authenticated
  USING (company_id::text = (auth.jwt()->>'company_id'));

-- RLS Policies for benchmarks (read-only for all authenticated users)
CREATE POLICY "Authenticated users can view benchmarks"
  ON benchmarks FOR SELECT
  TO authenticated
  USING (true);

-- RLS Policies for pricing_plans (read-only for all authenticated users)
CREATE POLICY "Authenticated users can view pricing plans"
  ON pricing_plans FOR SELECT
  TO authenticated
  USING (true);

-- RLS Policies for extensions (read-only for all authenticated users)
CREATE POLICY "Authenticated users can view extensions"
  ON extensions FOR SELECT
  TO authenticated
  USING (true);

-- Insert default benchmarks
INSERT INTO benchmarks (metric_name, min_value, max_value, ideal_value, critical_value) VALUES
  ('TC Usuários (%)', 8.00, 15.00, 10.50, NULL),
  ('TC Leads (%)', 4.50, 6.00, 5.25, NULL),
  ('CAC', 250.00, 500.00, 350.00, NULL),
  ('CAC:LTV', 3.00, 7.00, 4.00, 3.00),
  ('ROI (%)', 300.00, 500.00, 400.00, NULL),
  ('Ticket Médio', 120.00, 200.00, 150.00, NULL)
ON CONFLICT (metric_name) DO NOTHING;

-- Insert default pricing plans
INSERT INTO pricing_plans (name, price) VALUES
  ('MEI', 69.90),
  ('Simples Nacional', 119.90),
  ('Lucro Real/Presumido', 179.90)
ON CONFLICT (name) DO NOTHING;

-- Insert default extensions
INSERT INTO extensions (name, price) VALUES
  ('Controle de Estoque', 15.99),
  ('Controle Financeiro', 15.99),
  ('Emissão de Boleto Bancário', 15.99),
  ('Comissão de Vendedores', 15.99),
  ('Nota Fiscal de Serviço', 39.90),
  ('PDV', 39.90),
  ('Força de Vendas', 39.90)
ON CONFLICT (name) DO NOTHING;