from dotenv import load_dotenv
from phoenix.otel import register

load_dotenv()

# configure the Phoenix tracer
tracer_provider = register(
    project_name="sbotify", # Default is 'default'
    protocol="http/protobuf",
)
tracer = tracer_provider.get_tracer(__name__)