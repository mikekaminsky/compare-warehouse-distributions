# TODO:
1. Set up scripting
  * [x] Use vlad to create a cluster with appropriate ip whitelist
    * [ ] TODO: Have vlad read off of a local config file that python scripts will also have access to.
    * [ ] TODO: Set up WLM
  * Python script to copy/load data from the fivetran repo
    * https://github.com/fivetran/benchmark/blob/master/200-PopulateRedshiftSimple.sh
2. Conform the data
  * Set up DBT project to transform data into two schemas (star & denormed)
3. Write queries for test
  * Target BI-style queries 
  * Test different cardinalities
4. Test query time
  * Python script
5. Write the blog-post
  * Python script
