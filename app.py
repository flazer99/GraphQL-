import typing
import storage
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Mesh:
    value: typing.List[float]
    url: str

@strawberry.type
class Query:
    @strawberry.field
    def mesh(self, info) -> typing.List[Mesh]:
        return list(map(lambda x: Mesh(value = x['value'], url = x['url']), storage.data_store))

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_mesh(self, value: typing.List[float], url: str) -> Mesh:
        print("Adding the record: Value = {}, URL = {}".format(value, url))
        mesh_obj = Mesh(value = value, url = url)
        storage.data_store.append({'value': mesh_obj.value, 'url': mesh_obj.url})
        return mesh_obj

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")