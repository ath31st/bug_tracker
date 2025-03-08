from marshmallow import Schema, fields


class CommentSchema(Schema):
    id = fields.Int()
    content = fields.Str()
    issue_id = fields.Int()
    author_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
