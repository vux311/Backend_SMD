from marshmallow import Schema, fields
from marshmallow.validate import Length

class SyllabusSchema(Schema):
    id = fields.Int(dump_only=True)
    subject_id = fields.Int(required=True)
    program_id = fields.Int(required=True)
    academic_year_id = fields.Int(required=True)
    lecturer_id = fields.Int(required=True)

    status = fields.Str(dump_only=True)
    version = fields.Str(load_default="1.0", validate=Length(max=10))
    time_allocation = fields.Str(load_default=None)
    prerequisites = fields.Str(load_default=None)
    publish_date = fields.DateTime(load_default=None)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)