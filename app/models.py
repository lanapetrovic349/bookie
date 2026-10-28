# models.py
from django.conf import settings
from django.db import models

class AppQuiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = "app_quiz"          # postojeća tabela
        # managed = False               # stavi False ako NE želiš da Django pravi migracije za ovu tabelu

    def __str__(self):
        return self.title


class AppTeam(models.Model):
    name = models.CharField(max_length=255)
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        db_column="owner_user_id",
        related_name="owned_teams",
    )
    quiz = models.ForeignKey(
        AppQuiz,
        on_delete=models.CASCADE,
        db_column="quiz_id",
        related_name="teams",
    )

    class Meta:
        db_table = "app_team"
        # managed = False

    def __str__(self):
        return self.name


class AppMembership(models.Model):
    # NOVO: jednostavan PK
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="memberships",
    )
    team = models.ForeignKey(
        AppTeam,
        on_delete=models.CASCADE,
        db_column="team_id",
        related_name="memberships",
    )
    quiz = models.ForeignKey(
        AppQuiz,
        on_delete=models.CASCADE,
        db_column="quiz_id",
        related_name="memberships",
    )

    class Meta:
        db_table = "app_membership"
        unique_together = (("user", "team", "quiz"),)
        # managed = False
