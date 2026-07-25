graph TD
    %% Styling Configuration
    classDef client fill:#f9fafb,stroke:#d1d5db,stroke-width:2px,color:#000000;
    classDef backend fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a;
    classDef database fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b;

    %% Architecture Flow Node Layout
    Browser[🌐 User Browser <br> HTML5 / Tailwind CSS / JS]:::client
    
    subgraph FastAPI_Backend_Infrastructure [FastAPI Application Framework]
        Router[🛡️ API Routing Layer <br> Request Parsing & Pydantic Validation]:::backend
        Template[📄 Template Handler <br> Serve index.html via Jinja2]:::backend
        Shortener[⚙️ Shortening Engine <br> Base62 Encoding & Collision Check]:::backend
        Redirector[🔀 Redirect Engine <br> HTTP 307 Handler & Analytics Tracker]:::backend
    end
    
    DB[(🗄️ Relational Persistence Layer <br> SQLAlchemy ORM / SQLite or Postgres)]:::database

    %% Connection Intersections
    Browser -- 1. Loads Webpage / Request GET / --> Template
    Browser -- 2. Submits Long URL / Request POST /shorten / --> Router
    Browser -- 4. Clicks Short Link / Request GET /short_code / --> Router
    
    Router --> Shortener
    Router --> Redirector
    
    Shortener -- 3. Commits New Unique Mapping Record --> DB
    Redirector -- 5. Increments 'clicks' Count & Reads Original Target --> DB
    Redirector -. 6. Responds Location Routing Header .-> Browser
