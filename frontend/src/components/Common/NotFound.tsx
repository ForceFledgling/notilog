import { Button, Container, Text } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"

const NotFound = () => {
  return (
    <>
      <Container
        h="100vh"
        alignItems="stretch"
        justifyContent="center"
        textAlign="center"
        maxW="sm"
        centerContent
      >
        <Text
          fontSize="8xl"
          color="ui.main"
          fontWeight="bold"
          lineHeight="1"
          mb={4}
        >
          404
        </Text>
        <Text fontSize="md">Упс!</Text>
        <Text fontSize="md">Страница не найдена.</Text>
        <Button
          as={Link}
          to="/"
          color="ui.main"
          borderColor="ui.main"
          variant="outline"
          mt={4}
        >
          На главную
        </Button>
      </Container>
    </>
  )
}

export default NotFound
