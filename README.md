# GraphQL-to-SPARQL (Master's Thesis)

Thema : "Processing of mapping an existing SparQL Open Data endpoint to GraphQL endpoint without losing data integrity"

A Django project that maps an existing SPARQL/Open Data endpoint to a GraphQL schema while preserving data structure and integrity. The project fetches SPARQL query results, saves them into Django models and exposes a GraphQL API for easier consumption by frontends and applications.

**Motivation**
The rigid structure of SPARQL queries and the need to comprehend data schemas make it difficult for frontend or application end users to utilise open data effectively. Moreover, small-level organizations and projects may lack tools or expertise to craft SPARQL queries; exposing the same data through a GraphQL layer makes discovery and consumption easier while preserving the original data integrity.


<img width="661" alt="Screenshot 2025-07-07 at 7 42 36 PM" src="https://github.com/user-attachments/assets/8e768668-82d6-4ce1-97ee-75b1b8b93738" />

Frontend Design
<img width="1370" alt="Screenshot 2025-06-27 at 3 56 20 PM" src="https://github.com/user-attachments/assets/e6585099-4ad6-4eb0-b6df-cdb49f2830db" />


## Features
- Fetches dataset entries from a SPARQL endpoint (example uses data.europa.eu)
- Converts SPARQL JSON results into Django models: Head, PropertyType, Binding, Results, Data
- GraphQL schema (graphql_main/schema.py) to query:
  - head (vars, link)
  - results (bindings, grouped views, filters)
- Helper scripts to read RDF files and query the data.europa.eu API
- Example RDF/CSV/GeoJSON sample data included in the repo

## Quick start (development)
1. Clone the repository
   ```bash
   git clone https://github.com/dooa-ansari/graphqltosparql.git
   cd graphqltosparql
   ```

2. Create and activate a Python virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies
   Note: The repository currently doesn't include a `requirements.txt`. Install the main dependencies:
   ```bash
   pip install Django graphene-django SPARQLWrapper pymantic requests
   ```

4. Apply migrations and run the dev server
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Populate the database with SPARQL results
   - Use the provided view to call the SPARQL wrapper:
     ```
     GET /get_rdf_data?dataset=<graph-URI>
     ```
   - Example:
     ```
     http://127.0.0.1:8000/get_rdf_data?dataset=https://data.europa.eu/example-graph
     ```
   - The view `sparql_main.views.get_rdf_data` calls `sparql_main.wrapper.sparqlWrapperTest(...)` which fetches data, parses bindings, and saves them to the DB (models in `sparql_main/models.py`).

6. Expose the GraphQL API
   - The GraphQL schema is defined in `graphql_main/schema.py` (schema = graphene.Schema(query=Query)).
   - Add a URL route to project `urls.py` to mount Graphene's GraphQLView at `/graphql/` (if not already present):
     ```python
     from graphene_django.views import GraphQLView
     urlpatterns += [path("graphql/", GraphQLView.as_view(graphiql=True))]
     ```

## Example GraphQL query
```graphql
query {
  head {
    vars
    link
  }
  results {
    distinct
    ordered
    bindings(orderBy: "title__value") {
      title {
        value
        xmlLang
      }
      description {
        value
      }
      accessURL {
        value
      }
      maintainerEmail {
        value
      }
    }
    groupedBindings {
      xmlLang
      bindings {
        title { value }
      }
    }
  }
}
```

## Important files & structure
- manage.py — Django entrypoint
- graphql_main/schema.py — GraphQL types, resolvers and schema
- sparql_main/wrapper.py — SPARQLWrapper usage; transforms SPARQL JSON into Django models
- sparql_main/models.py — Head, PropertyType, Binding, Results, Data
- sparql_main/views.py — view endpoints (get_rdf_data, available graph IRIs)
- sample data files: `response_data.rdf`, `tierpark.rdf`, `check.rdf`, `Tierparks.csv`, `parcs-animaliers.geojson`, and `db.sqlite3` (example DB)

## Development notes & TODOs
- Add a `requirements.txt` with pinned versions for reproducibility.
- Add project-level `urls.py` entry for GraphQL if missing.
- Consider handling optional/missing binding fields more defensively in `wrapper.py` (there are places where keys may be absent or have casing inconsistencies like `accessUrl` vs `accessURL`).
- Add unit tests and a simple CI workflow to run migrations + tests.
- Add a LICENSE (MIT, CC-BY, or university-approved license), and an author/contributor section.

## Troubleshooting
- If Django complains about missing settings module: ensure `sparqltographql` project folder and `sparqltographql/settings.py` exist and are discoverable by Python path.
- If SPARQL queries fail due to SSL, wrapper.py currently attempts to disable SSL verification in environments that lack a proper context — be cautious for production.

## License
No license file detected in the repository. Add a LICENSE file if you intend to publish or permit reuse.

---
