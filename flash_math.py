import play
import random
import time
import pygame
import math

# Saved scores at:
# Bowen Math Flash
# https://docs.google.com/spreadsheets/d/1hKc3RliioqCvMZnLoj-nutV5Dba-UwmaZBcG9qxBQbA/edit#gid=0


numbers_to_study = [  6, 7, 8, 9]
max_bottom_number = 11
num_questions = 20

# Constants on screen
play.new_text("x", y=30, x=-100, font_size=100, color='darkgreen')
play.new_line("darkgreen", x=-80, y=-0,thickness=5, length=150)
correct_sound = pygame.mixer.Sound("magic.wav")
incorrect_sound = pygame.mixer.Sound("DunDunDunnn.wav")


class MathTest:
    """ This class represents your entire experience (start to finish)"""

    def __init__(self):
        self.questions_remaining = num_questions
        self.questions_correct = 0
        self.questions_incorrect = 0
        self.questions_correct_text = play.new_text("Correct: 0  ", y=play.screen.top - 30, x=play.screen.left + 150, font_size=40, font="Minecraft.ttf", color="green")
        self.questions_incorrect_text = play.new_text("Incorrect: 0", y=play.screen.top - 80, x=play.screen.left + 150, font_size=40, font="Minecraft.ttf", color="red")
        self.questions_remaining_text = play.new_text(f"Questions Remaining: {num_questions}", y=play.screen.bottom + 50, x=play.screen.left / 2,
                                                    font_size=40)

    def update_view(self):
        self.questions_correct_text.words = f"Correct: {self.questions_correct}  "
        self.questions_incorrect_text.words = f"Incorrect: {self.questions_incorrect}"
        self.questions_remaining_text.words = f"Questions Remaining: {self.questions_remaining}"


class TotalTimeDisplay:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.display_text = play.new_text("1:23", y=play.screen.top - 30, x=play.screen.right - 50, font_size=40, font="Minecraft.ttf")

    def update_time(self):
        current_time_s = math.ceil(time.time() - self.start_time)
        if self.end_time is not None:
            current_time_s = math.ceil(self.end_time - self.start_time)
        self.display_text.words = f"{current_time_s // 60}:{current_time_s % 60:02}"


class MathRound:
    """ This class represents a single round (one question)"""

    def __init__(self):
        self.top = random.choice(numbers_to_study)
        self.bottom = random.randint(0, max_bottom_number)
        self.guess = ""
        self.answer = str(self.top * self.bottom)
        self.index = 0
        self.correct = False
        self.incorrect = False

    def key_pressed(self, key):
        self.guess += key
        if key == self.answer[self.index]:
            self.index += 1
            # print("Correct so far")
            if self.index >= len(self.answer):
                # print("Completely correct")
                self.correct = True
        else:
            # print("Incorrect")
            self.incorrect = True


class Controller():

    def __init__(self):
        self.math_round = MathRound()
        self.time_display = TotalTimeDisplay()
        self.math_test = MathTest()
        self.top_number_text = play.new_text("", y=150, font_size=160, color='darkgreen')
        self.bottom_number_text = play.new_text("", y=50, font_size=160, color='darkgreen')
        self.answer_text = play.new_text("", y=-70, font_size=160, color='darkgreen')
        self.feedback_text = play.new_text("", y=-150, font_size=100)

        self.update_numbers()

    async def key_pressed(self, key):
        self.math_round.key_pressed(key)
        await self.update_view()

    def update_numbers(self):
        self.top_number_text.words = self.math_round.top
        self.bottom_number_text.words = self.math_round.bottom
        self.answer_text.words = self.math_round.guess

    async def update_view(self):
        self.update_numbers()

        if self.math_round.correct:
            # await play.timer(seconds=0.25)
            self.feedback_text.color = "green"
            self.feedback_text.words = "Correct"
            self.math_test.questions_correct += 1
            self.math_test.questions_remaining -= 1
            self.math_test.update_view()
            correct_sound.play()
            await play.timer(seconds=0.25)
            if self.math_test.questions_remaining != 0:
                self.math_round = MathRound()
                self.update_numbers()
            self.feedback_text.words = ""

        if self.math_round.incorrect:
            # await play.timer(seconds=0.25)
            self.feedback_text.color = "red"
            self.feedback_text.words = "Incorrect"
            self.math_test.questions_incorrect += 1
            self.math_test.questions_remaining -= 1
            self.math_test.update_view()
            incorrect_sound.play()
            await play.timer(seconds=2.5)
            if self.math_test.questions_remaining != 0:
                self.math_round = MathRound()
                self.update_numbers()
            self.feedback_text.words = ""

        if self.math_test.questions_remaining == 0:
            self.time_display.end_time = time.time()

controller = Controller()


@play.repeat_forever
def do():
    controller.time_display.update_time()


@play.when_any_key_pressed
async def do(key):
    await controller.key_pressed(key)

play.start_program()
