from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from models import IssueStatus, Priority


class IssueSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    status = EnumField(IssueStatus)
    priority = EnumField(Priority)
    reporter_id = fields.Int()
    assignee_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
