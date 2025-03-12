from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from models import IssueStatus, Priority


class FullIssueSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    status = EnumField(IssueStatus)
    priority = EnumField(Priority)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    reporter = fields.Nested("UserSchema")
    assignee = fields.Nested("UserSchema")
    comments = fields.Nested("CommentSchema", many=True)
