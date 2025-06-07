"""Initial tables

Revision ID: 1544659e4f2f
Revises: 
Create Date: 2025-06-06 19:42:13.353782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1544659e4f2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # CREATE tables and indexes here
    op.create_table('users',
        sa.Column('user_id', sa.INTEGER(), server_default=sa.text("nextval('users_user_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
        sa.Column('role', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column('phone_number', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.Column('hashed_password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('registration_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
        sa.UniqueConstraint('email', name='users_email_key'),
        sa.UniqueConstraint('username', name='users_username_key'),
        postgresql_ignore_search_path=False
    )
    op.create_table('appointments',
        sa.Column('appointment_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('doctor_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('appointment_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.CheckConstraint("status::text = ANY (ARRAY['Scheduled'::character varying, 'Completed'::character varying, 'Cancelled'::character varying]::text[])", name='appointments_status_check'),
        sa.ForeignKeyConstraint(['doctor_id'], ['users.user_id'], name='appointments_doctor_id_fkey'),
        sa.ForeignKeyConstraint(['patient_id'], ['users.user_id'], name='appointments_patient_id_fkey'),
        sa.PrimaryKeyConstraint('appointment_id', name='appointments_pkey')
    )
    op.create_table('prescriptions',
        sa.Column('prescription_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('doctor_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('medication', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('dosage', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['doctor_id'], ['users.user_id'], name='prescriptions_doctor_id_fkey'),
        sa.ForeignKeyConstraint(['patient_id'], ['users.user_id'], name='prescriptions_patient_id_fkey'),
        sa.PrimaryKeyConstraint('prescription_id', name='prescriptions_pkey')
    )
    op.create_table('medical_history',
        sa.Column('history_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('condition', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('treatment', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('start_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column('end_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='medical_history_user_id_fkey'),
        sa.PrimaryKeyConstraint('history_id', name='medical_history_pkey')
    )
    op.create_table('reminders',
        sa.Column('reminder_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('reminder_text', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('reminder_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='reminders_user_id_fkey'),
        sa.PrimaryKeyConstraint('reminder_id', name='reminders_pkey')
    )
    op.create_table('allergy_tracking',
    sa.Column('allergy_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('allergy_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('reaction', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='allergy_tracking_user_id_fkey'),
    sa.PrimaryKeyConstraint('allergy_id', name='allergy_tracking_pkey')
    )
    op.create_table('lab_results',
        sa.Column('result_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('test_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
        sa.Column('result_data', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='lab_results_user_id_fkey'),
        sa.PrimaryKeyConstraint('result_id', name='lab_results_pkey')
    )
    op.create_table('health_monitoring_logs',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('monitoring_data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
        sa.Column('logged_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='health_monitoring_logs_user_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='health_monitoring_logs_pkey')
    )
    op.create_table('patient_uploaded_docs',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('document_data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
        sa.Column('uploaded_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='patient_uploaded_docs_user_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='patient_uploaded_docs_pkey')
    )
    op.create_table('ehr',
        sa.Column('record_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('patient_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('diagnosis', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('treatment', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('notes', sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['patient_id'], ['users.user_id'], name='ehr_patient_id_fkey'),
        sa.PrimaryKeyConstraint('record_id', name='ehr_pkey')
    )
    op.create_table('diagnostic_insights',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('insights', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('generated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='diagnostic_insights_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='diagnostic_insights_pkey')
    )
    op.create_table('ehr_summary',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('ehr_data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='ehr_summary_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='ehr_summary_pkey')
    )
    op.create_table('ai_transcriptions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('transcription_data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='ai_transcriptions_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='ai_transcriptions_pkey')
    )
    op.create_table('followup_recommendations',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('recommendations', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=False),
        sa.Column('recommended_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='followup_recommendations_user_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='followup_recommendations_pkey')
    )
    op.create_table('ehr_summaries',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('ehr_data', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='ehr_summaries_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='ehr_summaries_pkey')
    )
    op.create_index('ix_ehr_summaries_id', 'ehr_summaries', ['id'], unique=False)
    op.create_table('otps',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('otp_code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('purpose', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expires_at', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='otps_pkey')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # DROP tables and indexes here
    op.drop_table('ehr')
    op.drop_table('users')
    op.drop_table('patient_uploaded_docs')
    op.drop_table('health_monitoring_logs')
    op.drop_table('appointments')
    op.drop_table('lab_results')
    op.drop_table('followup_recommendations')
    op.drop_table('prescriptions')
    op.drop_table('medical_history')
    op.drop_table('reminders')
    op.drop_table('otps')
    op.drop_table('ai_transcriptions')
    op.drop_table('ehr_summary')
    op.drop_table('diagnostic_insights')
    op.drop_table('allergy_tracking')
    op.drop_index('ix_ehr_summaries_id', table_name='ehr_summaries')
    op.drop_table('ehr_summaries')
