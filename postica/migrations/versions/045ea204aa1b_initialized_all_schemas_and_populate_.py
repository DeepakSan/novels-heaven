from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '045ea204aa1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables
    op.create_table('novel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('chinese_name', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('picture', sa.LargeBinary(), nullable=True),
    sa.Column('date_edited', sa.DateTime(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_table('novelchapter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('novel_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('previous_chapter_id', sa.Integer(), nullable=True),
    sa.Column('next_chapter_id', sa.Integer(), nullable=True),
    sa.Column('chapter_title', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['next_chapter_id'], ['novelchapter.id'], ),
    sa.ForeignKeyConstraint(['novel_id'], ['novel.id'], ),
    sa.ForeignKeyConstraint(['previous_chapter_id'], ['novelchapter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # Insert sample data for novels
    novel_data = [
        ('The Great Adventure', '伟大的冒险', 'An epic tale of courage and friendship.', datetime.now(), datetime.now()),
        ('Mystery of the Lost City', '失落城市的谜', 'A thrilling mystery novel full of suspense.', datetime.now(), datetime.now()),
        ('The Dragon Chronicles', '龙的编年史', 'A fantasy novel about dragons and kingdoms.', datetime.now(), datetime.now()),
        ('Space Odyssey', '太空奥德赛', 'A science fiction journey across the universe.', datetime.now(), datetime.now()),
        ('Tales of the Sea', '海的传说', 'A collection of stories set on the high seas.', datetime.now(), datetime.now()),
    ]

    op.bulk_insert(
        sa.table('novel',
            sa.column('name'),
            sa.column('chinese_name'),
            sa.column('description'),
            sa.column('date_edited'),
            sa.column('date_created')
        ),
        [{
            'name': name,
            'chinese_name': chinese_name,
            'description': description,
            'date_edited': date_edited,
            'date_created': date_created
        } for name, chinese_name, description, date_edited, date_created in novel_data]
    )
    
    novelchapter_table = sa.table(
        'novelchapter',
        sa.column('id'),
        sa.column('novel_id'),
        sa.column('chapter_title'),
        sa.column('content'),
        sa.column('previous_chapter_id'),
        sa.column('next_chapter_id')
    )

    # Insert sample data for chapters without setting next and previous IDs
    for novel_id in range(1, 6):
        for i in range(1, 11):
            chapter_title = f'Chapter {i}'
            content = f'This is the content of {chapter_title} for Novel {novel_id}.'
            op.execute(
                novelchapter_table.insert().values(
                    novel_id=novel_id,
                    chapter_title=chapter_title,
                    content=content,
                    previous_chapter_id=None,
                    next_chapter_id=None
                )
            )

    for novel_id in range(1, 6):
        for i in range(1, 10):  # Skip the last chapter since it has no next chapter
            # Update next_chapter_id
            op.execute(
                sa.text("""
                    UPDATE novelchapter
                    SET next_chapter_id = :next_chapter_id
                    WHERE novel_id = :novel_id AND id = :chapter_id
                """).bindparams(
                    next_chapter_id=i + 1,
                    novel_id=novel_id,
                    chapter_id=i
                )
            )
            
            # Update previous_chapter_id
            if i > 1:
                op.execute(
                    sa.text("""
                        UPDATE novelchapter
                        SET previous_chapter_id = :previous_chapter_id
                        WHERE novel_id = :novel_id AND id = :chapter_id
                    """).bindparams(
                        previous_chapter_id=i - 1,
                        novel_id=novel_id,
                        chapter_id=i
                    )
                )

def downgrade():
    # Drop tables
    op.drop_table('novelchapter')
    op.drop_table('novel')
