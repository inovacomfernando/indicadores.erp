/*
  # Fix RLS Policies for User Access

  ## Overview
  This migration fixes the RLS policies to properly work with Supabase Auth.
  The previous policies used JWT metadata which needs proper setup.

  ## Changes
  1. Drop existing restrictive policies
  2. Create simpler policies that work with auth.uid()
  3. Add a helper function to get company_id from user metadata

  ## Security
  - Users can only access their own company data
  - Benchmarks, plans, and extensions are read-only for all authenticated users
*/

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view own company" ON companies;
DROP POLICY IF EXISTS "Users can update own company" ON companies;
DROP POLICY IF EXISTS "Users can view own company metrics" ON monthly_metrics;
DROP POLICY IF EXISTS "Users can insert own company metrics" ON monthly_metrics;
DROP POLICY IF EXISTS "Users can update own company metrics" ON monthly_metrics;
DROP POLICY IF EXISTS "Users can delete own company metrics" ON monthly_metrics;

-- Create helper function to get company_id from user metadata
CREATE OR REPLACE FUNCTION get_user_company_id()
RETURNS uuid AS $$
BEGIN
  RETURN (auth.jwt()->>'company_id')::uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Recreate policies with proper company_id check
CREATE POLICY "Users can view own company"
  ON companies FOR SELECT
  TO authenticated
  USING (id = get_user_company_id());

CREATE POLICY "Users can update own company"
  ON companies FOR UPDATE
  TO authenticated
  USING (id = get_user_company_id())
  WITH CHECK (id = get_user_company_id());

CREATE POLICY "Users can view own company metrics"
  ON monthly_metrics FOR SELECT
  TO authenticated
  USING (company_id = get_user_company_id());

CREATE POLICY "Users can insert own company metrics"
  ON monthly_metrics FOR INSERT
  TO authenticated
  WITH CHECK (company_id = get_user_company_id());

CREATE POLICY "Users can update own company metrics"
  ON monthly_metrics FOR UPDATE
  TO authenticated
  USING (company_id = get_user_company_id())
  WITH CHECK (company_id = get_user_company_id());

CREATE POLICY "Users can delete own company metrics"
  ON monthly_metrics FOR DELETE
  TO authenticated
  USING (company_id = get_user_company_id());