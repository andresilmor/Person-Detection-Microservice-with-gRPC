import strawberry
from strawberry.extensions import Extension
from graphql import GraphQLError


class VisibleError(Exception):
	pass

class MaskErrors(Extension):
	def on_request_end(self):
		result = self.execution_context.result
		if result.errors:
			processed_errors = []
			for error in result.errors:
				
				if error.original_error and not isinstance(error.original_error, VisibleError):
					processed_errors.append(
						GraphQLError(
							message="Unexpected error.",
							nodes=error.nodes,
							source=error.source,
							positions=error.positions,
							path=error.path,
							original_error=None
						)
					)
				else:
					processed_errors.append(error)

			result.errors = processed_errors

@strawberry.type
class ErrorMessage:
    message: str

