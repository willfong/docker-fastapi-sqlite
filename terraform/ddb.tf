resource "aws_dynamodb_table" "users" {
  name           = "Users"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "id"
  attribute {
    name = "id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "messages" {
  name           = "Messages"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "id"
  range_key      = "datetime"
  attribute {
    name = "id"
    type = "S"
  }
  attribute {
    name = "datetime"
    type = "S"
  }
}
