from marshmallow import Schema, fields


class NewCommentSchema(Schema):
    content = fields.Str(required=True)
    issue_id = fields.Int(required=True, data_key="issueId")
