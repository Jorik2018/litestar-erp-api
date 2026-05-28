import os
import traceback
from dotenv import load_dotenv
from gqlalchemy import Memgraph


load_dotenv()


class MemgraphService:
    def __init__(self) -> None:
        self.host = os.getenv("MEMGRAPH_HOST", "localhost")
        self.port = int(os.getenv("MEMGRAPH_PORT", "7687"))
        self.username = os.getenv("MEMGRAPH_USERNAME", "")
        self.password = os.getenv("MEMGRAPH_PASSWORD", "")
        self.encrypted = os.getenv("MEMGRAPH_ENCRYPTED", "false").lower() == "true"

    def _get_connection(self) -> Memgraph:
        print("MEMGRAPH_HOST:", self.host)
        print("MEMGRAPH_PORT:", self.port)
        print("MEMGRAPH_USERNAME:", self.username)
        print("MEMGRAPH_ENCRYPTED:", self.encrypted)

        return Memgraph(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            encrypted=self.encrypted,
        )

    def test_connection(self) -> dict[str, str]:
        try:
            connection = self._get_connection()
            results = connection.execute_and_fetch("RETURN 'Memgraph OK' AS message")
            message = next(results)["message"]
            return {"message": message}
        except Exception as exc:
            print("Error en test_connection:", exc)
            traceback.print_exc()
            raise

    def create_person(self, person_id: int, name: str, age: int) -> dict:
        try:
            connection = self._get_connection()
            query = """
            CREATE (p:Person {id: $id, name: $name, age: $age})
            RETURN p.id AS id, p.name AS name, p.age AS age
            """
            results = connection.execute_and_fetch(
                query,
                {"id": person_id, "name": name, "age": age},
            )
            return next(results)
        except Exception as exc:
            print("Error en create_person:", exc)
            traceback.print_exc()
            raise

    def list_people(self) -> list[dict]:
        try:
            connection = self._get_connection()
            query = """
            MATCH (p:Person)
            RETURN p.id AS id, p.name AS name, p.age AS age
            ORDER BY p.id
            """
            results = connection.execute_and_fetch(query)
            return list(results)
        except Exception as exc:
            print("Error en list_people:", exc)
            traceback.print_exc()
            raise

    def get_person(self, person_id: int) -> dict | None:
        try:
            connection = self._get_connection()
            query = """
            MATCH (p:Person {id: $id})
            RETURN p.id AS id, p.name AS name, p.age AS age
            LIMIT 1
            """
            results = list(connection.execute_and_fetch(query, {"id": person_id}))
            return results[0] if results else None
        except Exception as exc:
            print("Error en get_person:", exc)
            traceback.print_exc()
            raise

    def update_person(
        self,
        person_id: int,
        name: str | None = None,
        age: int | None = None,
    ) -> dict | None:
        try:
            connection = self._get_connection()

            person = self.get_person(person_id)
            if not person:
                return None

            new_name = name if name is not None else person["name"]
            new_age = age if age is not None else person["age"]

            query = """
            MATCH (p:Person {id: $id})
            SET p.name = $name, p.age = $age
            RETURN p.id AS id, p.name AS name, p.age AS age
            """
            results = connection.execute_and_fetch(
                query,
                {"id": person_id, "name": new_name, "age": new_age},
            )
            return next(results)
        except Exception as exc:
            print("Error en update_person:", exc)
            traceback.print_exc()
            raise

    def delete_person(self, person_id: int) -> bool:
        try:
            connection = self._get_connection()

            person = self.get_person(person_id)
            if not person:
                return False

            query = """
            MATCH (p:Person {id: $id})
            DELETE p
            """
            connection.execute(query, {"id": person_id})
            return True
        except Exception as exc:
            print("Error en delete_person:", exc)
            traceback.print_exc()
            raise
