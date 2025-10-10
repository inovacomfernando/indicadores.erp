/*
  # Allow Public Company Creation

  ## Overview
  This migration allows new users to create companies during signup.
  Since users are not authenticated yet during signup, we need to allow
  public inserts to the companies table temporarily during the signup process.

  ## Changes
  1. Add policy to allow insert for anon users (signup process)
  2. Keep existing policies for authenticated users

  ## Security Notes
  - This allows anyone to create a company record
  - The company_id is immediately associated with the user during signup
  - RLS still protects reading and updating to authenticated users only
*/

-- Allow anon users to insert companies (for signup)
CREATE POLICY "Allow public company creation during signup"
  ON companies FOR INSERT
  TO anon
  WITH CHECK (true);