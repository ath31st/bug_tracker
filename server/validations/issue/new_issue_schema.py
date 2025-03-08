from marshmallow import fields, Schema
from marshmallow_enum import EnumField
from models import IssueStatus, Priority


class NewIssueSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = EnumField(IssueStatus, required=True)
    priority = EnumField(Priority, required=True)
    reporter_id = fields.Int(required=True)
