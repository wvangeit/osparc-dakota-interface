import numpy as np
import os
import osparc
import time
from osparc.api import UsersApi
from osparc.api import FilesApi, SolversApi
from osparc.models import File, Job, JobInputs, JobOutputs, JobStatus, Solver

def rsinc(x: list[float], a: float) -> float:
    
    cfg = osparc.Configuration(
        host="https://api.osparc-master.speag.com",
        username="07c83ea3-cd07-582b-aeeb-2232827a30dd",
        password="9e394ecf-b693-5ebb-b899-daab41efced8",
    )
    
    with osparc.ApiClient(cfg) as api_client:

        solvers_api = SolversApi(api_client)
        solver: Solver = solvers_api.get_solver_release(
            "simcore/services/comp/cctest-sinc", "0.1.0"
        )

        job: Job = solvers_api.create_job(
            solver.id,
            solver.version,
            JobInputs(
                {
                    "x": x,
                    "a": a,
                }
            ),
        )

        status: JobStatus = solvers_api.start_job(solver.id, solver.version, job.id)
        while not status.stopped_at:
            time.sleep(1)
            status = solvers_api.inspect_job(solver.id, solver.version, job.id)
            print("Solver progress", f"{status.progress}/100", flush=True)

        outputs: JobOutputs = solvers_api.get_job_outputs(solver.id, solver.version, job.id)

        print(f"Job {outputs.job_id} got these results:")
        for output_name, result in outputs.results.items():
            print(output_name, "=", result)
            
        return outputs.results["out_1"]

