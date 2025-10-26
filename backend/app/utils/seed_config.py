import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_sync_engine
from app.models.configuration import Base, Configuration

async def seed_default_configuration():
    """
    Seed default configuration values into the database
    """
    from app.utils.config_loader import get_default_config
    
    engine = get_sync_engine()
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    # Get default config
    default_config = await get_default_config()
    
    # Insert default configuration values
    from sqlalchemy import create_engine, text
    
    sync_engine = create_engine(str(engine.url))
    
    try:
        with sync_engine.connect() as conn:
            # Clear existing config
            conn.execute(text("DELETE FROM configuration"))
            
            # Insert new config
            for key, value in default_config.items():
                if key in ["LLM_TOOL_DEFINITION", "LLM_SYSTEM_PROMPT", "LLM_USER_PROMPT_TEMPLATE"]:
                    # These are multi-line strings, store as-is
                    conn.execute(
                        text("""
                            INSERT INTO configuration (key, value, group) 
                            VALUES (:key, :value, :group)
                        """),
                        {
                            "key": key,
                            "value": value,
                            "group": "prompt"
                        }
                    )
                else:
                    conn.execute(
                        text("""
                            INSERT INTO configuration (key, value, group) 
                            VALUES (:key, :value, :group)
                        """),
                        {
                            "key": key,
                            "value": value,
                            "group": "api"
                        }
                    )
            
            conn.commit()
            print("✅ Default configuration seeded successfully!")
            
    except Exception as e:
        print(f"❌ Error seeding configuration: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(seed_default_configuration())