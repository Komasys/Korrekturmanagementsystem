"""empty message

Revision ID: 7f9dff255693
Revises: cb40be266b43
Create Date: 2025-03-19 11:12:24.736414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f9dff255693'
down_revision = 'cb40be266b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('benutzer',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('rolle', sa.Enum('STUDENT', 'TUTOR', 'DOZENT', 'QM', 'ADMIN', name='rolle'), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('letzte_anmeldung', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('kurs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('kuerzel', sa.String(length=50), nullable=False),
    sa.Column('kursleitung_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['kursleitung_id'], ['benutzer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('kuerzel')
    )
    op.create_table('lernmaterial',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('titel', sa.String(length=255), nullable=False),
    sa.Column('typ', sa.Enum('PDF', 'VIDEO', 'PRAESENTATION', 'QUIZ', name='lernmaterialtyp'), nullable=False),
    sa.Column('kurs_id', sa.UUID(), nullable=False),
    sa.Column('erstelldatum', sa.DateTime(), nullable=False),
    sa.Column('letzter_aktualisierung', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['kurs_id'], ['kurs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('beschreibung', sa.Text(), nullable=False),
    sa.Column('kategorie', sa.Enum('TIPPFEHLER', 'INHALTLICHER_FEHLER', 'FORMATIERUNGSFEHLER', 'ERWEITERUNG', 'STRUKTURVERBESSERUNG', name='kategorie'), nullable=False),
    sa.Column('erstelldatum', sa.DateTime(), nullable=False),
    sa.Column('prioritaet', sa.Enum('NIEDRIG', 'MITTEL', 'HOCH', name='prioritaet'), nullable=True),
    sa.Column('kurs_id', sa.UUID(), nullable=False),
    sa.Column('ersteller_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['ersteller_id'], ['benutzer.id'], ),
    sa.ForeignKeyConstraint(['kurs_id'], ['kurs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('anhang',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('ticket_id', sa.UUID(), nullable=False),
    sa.Column('dateiname', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('historie',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('ticket_id', sa.UUID(), nullable=False),
    sa.Column('bearbeiter_id', sa.UUID(), nullable=False),
    sa.Column('beschreibung', sa.Text(), nullable=False),
    sa.Column('geaendert_am', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('NEU', 'ABGELEHNT', 'PRUEFUNG', 'ANPASSUNG', 'GESCHLOSSEN', name='ticketstatus'), nullable=False),
    sa.Column('pruefer_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['bearbeiter_id'], ['benutzer.id'], ),
    sa.ForeignKeyConstraint(['pruefer_id'], ['benutzer.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kommentar',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('benutzer_id', sa.UUID(), nullable=False),
    sa.Column('ticket_id', sa.UUID(), nullable=False),
    sa.Column('nachricht', sa.Text(), nullable=False),
    sa.Column('erstelldatum', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['benutzer_id'], ['benutzer.id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('kommentar')
    op.drop_table('historie')
    op.drop_table('anhang')
    op.drop_table('ticket')
    op.drop_table('lernmaterial')
    op.drop_table('kurs')
    op.drop_table('benutzer')
    # ### end Alembic commands ###
