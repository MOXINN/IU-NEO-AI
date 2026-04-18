# ============================================================================
# IU NWEO AI — Makefile
# Maintainer: Ops
# ============================================================================
# Convenience commands for the entire team.
# ============================================================================

.PHONY: help up down logs db-only backend frontend clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'



# --- Backend (local dev, outside Docker) ---
backend: ## Run FastAPI locally with hot-reload
	cd backend && uvicorn main:app --host 0.0.0.0 --port 8080 --reload

backend-install: ## Install backend Python dependencies
	cd backend && pip install -r requirements.txt

# --- Frontend (local dev, outside Docker) ---
frontend: ## Run Next.js dev server locally
	cd frontend && npm run dev

frontend-install: ## Install frontend dependencies
	cd frontend && npm install

# --- Utilities ---
clean: ## Keep for future python/node cleanup script
