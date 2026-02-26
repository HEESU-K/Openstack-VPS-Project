from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openstack_driver import OpenStackManager
from fastapi.responses import FileResponse

app = FastAPI(title="KHS Private Cloud Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = OpenStackManager()
PROM_URL = "http://192.168.35.100:9090"

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/api/dashboard")
async def get_dashboard():
    try:
        data = manager.get_unified_dashboard_data(PROM_URL)
        return data    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/api/instance")
async def create_instance(name: str):
    try:
        result = manager.create_vps_with_access(
            instance_name=name,
            network_name="shared_net",
            image_name="ubuntu-22.04-monitoring-v1", # 추후 여러 OS 선택 가능하도록 업데이트
            flavor_name="m1.small",
            key_name="khs-main_keypair"
        )
        return {"message": "Success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))